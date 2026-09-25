"""WBS↔LINK Challenge scorer. Trust first: confident wrong answers count most."""
from __future__ import annotations
import argparse,csv,io,json,os,subprocess,tarfile
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load_truth(which):
    if which=="practice":
        d=ROOT/"challenge/practice";return list(csv.DictReader(open(d/"answers_practice.csv",encoding="utf-8-sig"))),json.load(open(d/"events_practice.json",encoding="utf-8"))
    if not os.environ.get("HOLDOUT_KEY"): raise SystemExit("The hidden set can only be scored by the submission bot.")
    raw=subprocess.run(["openssl","enc","-d","-aes-256-cbc","-pbkdf2","-in",str(ROOT/"challenge/holdout/answers_holdout.enc"),"-pass","env:HOLDOUT_KEY"],capture_output=True,check=True).stdout
    tf=tarfile.open(fileobj=io.BytesIO(raw));return list(csv.DictReader(io.TextIOWrapper(tf.extractfile("answers_holdout.csv"),encoding="utf-8-sig"))),json.load(tf.extractfile("events_holdout.json"))
def src_of(v): return Path(v.strip()).name.rsplit("_M",1)[0] if v else ""
def norm(a):
    a=(a or "").strip().upper().replace(" ","");return "|".join(sorted(a.split("|"))) if a else ""
def score(answers_text,which,exceptions_text=None):
    truth,events=load_truth(which)
    counts=Counter((int(r["period"]),r["source"],(r.get("record_id") or "").strip()) for r in truth)
    excluded={k for k,n in counts.items() if not k[2] or n>1}
    t={(int(r["period"]),r["source"],(r.get("record_id") or "").strip()):norm(r["answer"]) for r in truth if (int(r["period"]),r["source"],(r.get("record_id") or "").strip()) not in excluded}
    sub={}
    for r in csv.DictReader(io.StringIO(answers_text)):
        r={(k or "").strip().lower():(v or "") for k,v in r.items()}
        try:k=(int(r.get("period",0)),src_of(r.get("source_file") or r.get("source","")),r.get("record_id","").strip())
        except ValueError:continue
        sub[k]=(norm(r.get("answer","")),(r.get("confidence") or "high").strip().lower())
    correct=wrong=silent=unsure=0
    for k,want in t.items():
        a,conf=sub.get(k,("",""))
        if a in ("","UNSURE"):unsure+=1
        elif a==want:correct+=1
        else:wrong+=1;silent+=int(conf in ("high",""))
    total=len(t);res={"set":which,"records":total,"correct":correct,"wrong":wrong,"silent_errors":silent,"unsure_or_blank":unsure,"precision":round(correct/(correct+wrong),4) if correct+wrong else 0.0,"coverage":round((correct+wrong)/total,4) if total else 0.0,"matched_rows":len(set(sub)&set(t))}
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
