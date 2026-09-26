"""WBS↔LINK Challenge scorer. Trust first: confident wrong mappings carry the largest penalty."""
from __future__ import annotations
import argparse,csv,io,json,os,subprocess,tarfile
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load_reference(which):
    if which=="practice":
        # Works both in the GitHub repo and in the standalone Practice download.
        candidates=[ROOT/"challenge/practice",ROOT/"practice"]
        d=next((p for p in candidates if (p/"answers_practice.csv").exists()),None)
        if d is None: raise FileNotFoundError("Could not find practice/answers_practice.csv. Run the scorer from the extracted Practice download or repository root.")
        return list(csv.DictReader(open(d/"answers_practice.csv",encoding="utf-8-sig"))),json.load(open(d/"events_practice.json",encoding="utf-8"))
    if not os.environ.get("HOLDOUT_KEY"): raise SystemExit("The hidden set can only be scored by the submission bot.")
    raw=subprocess.run(["openssl","enc","-d","-aes-256-cbc","-pbkdf2","-in",str(ROOT/"challenge/holdout/answers_holdout.enc"),"-pass","env:HOLDOUT_KEY"],capture_output=True,check=True).stdout
    tf=tarfile.open(fileobj=io.BytesIO(raw));return list(csv.DictReader(io.TextIOWrapper(tf.extractfile("answers_holdout.csv"),encoding="utf-8-sig"))),json.load(tf.extractfile("events_holdout.json"))

def src_of(v): return Path(v.strip()).name.rsplit("_M",1)[0] if v else ""

def norm(a):
    a=(a or "").strip().upper().replace(" ","")
    # Participant-facing term changed from LEGIT_ORPHAN to NO_WBS. Keep the legacy
    # reference value as an accepted alias so historical reference files remain valid.
    if a=="NO_WBS": a="LEGIT_ORPHAN"
    return "|".join(sorted(a.split("|"))) if a else ""

def score(answers_text,which,exceptions_text=None):
    reference,events=load_reference(which)
    counts=Counter((int(r["period"]),r["source"],(r.get("record_id") or "").strip()) for r in reference)
    excluded={k for k,n in counts.items() if not k[2] or n>1}
    t={(int(r["period"]),r["source"],(r.get("record_id") or "").strip()):norm(r["answer"]) for r in reference if (int(r["period"]),r["source"],(r.get("record_id") or "").strip()) not in excluded}
    sub={}
    for row_no,r in enumerate(csv.DictReader(io.StringIO(answers_text)),start=2):
        r={(k or "").strip().lower():(v or "") for k,v in r.items()}
        try:k=(int(r.get("period",0)),src_of(r.get("source_file") or r.get("source","")),r.get("record_id","").strip())
        except ValueError:continue
        a=norm(r.get("answer",""));conf=(r.get("confidence") or "").strip().lower()
        if a not in ("","UNSURE") and conf not in ("high","med","low"):
            raise ValueError(f"Row {row_no}: confidence must be high, med or low for an answered mapping. Got {conf or 'blank'}.")
        if a=="UNSURE" and conf not in ("","low"):
            raise ValueError(f"Row {row_no}: use blank or low confidence with UNSURE.")
        sub[k]=(a,conf)
    correct=wrong=silent=unsure=0
    high_correct=other_correct=other_wrong=0
    for k,want in t.items():
        a,conf=sub.get(k,("",""))
        if a in ("","UNSURE"):unsure+=1
        elif a==want:
            correct+=1
            if conf=="high": high_correct+=1
            else: other_correct+=1
        else:
            wrong+=1
            if conf=="high": silent+=1
            else: other_wrong+=1
    # Published trust-weighted score: reward supported mappings, strongly penalize
    # confident wrong mappings, and mildly penalize other wrong mappings.
    net_score=round(high_correct + 0.5*other_correct - 5*silent - 0.5*other_wrong,1)
    total=len(t);res={"set":which,"records":total,"correct":correct,"wrong":wrong,"silent_errors":silent,"unsure_or_blank":unsure,"net_score":net_score,"precision":round(correct/(correct+wrong),4) if correct+wrong else 0.0,"coverage":round((correct+wrong)/total,4) if total else 0.0,"matched_rows":len(set(sub)&set(t))}
    if exceptions_text:
        flagged=set()
        for r in csv.DictReader(io.StringIO(exceptions_text)):
            try:flagged.add((int(r.get("period",0) or 0),src_of(r.get("source_file","")),(r.get("record_id") or "").strip(),(r.get("type") or "").lower()))
            except ValueError:pass
        dup_found=sum(1 for p,s,i in excluded if any(fp==p and fs==s and fi==i for fp,fs,fi,_ in flagged))
        drift_found=sum(1 for e in events if any(fp==e["period"] and fs==e["source"] and ("drift" in ft or "structure" in ft or "code" in ft) for fp,fs,_,ft in flagged))
        res.update({"duplicate_ids_found":f"{dup_found}/{len(excluded)}","structural_changes_found":f"{drift_found}/{len(events)}"})
    return res

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("answers");ap.add_argument("--set",default="practice",choices=["practice","holdout"]);ap.add_argument("--exceptions");a=ap.parse_args()
    print(json.dumps(score(open(a.answers,encoding="utf-8-sig").read(),a.set,open(a.exceptions,encoding="utf-8-sig").read() if a.exceptions else None),indent=1))
