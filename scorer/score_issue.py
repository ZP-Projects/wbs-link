"""WBS↔LINK submission bot. Hidden challenge: one scored attempt per GitHub user."""
import json,os,re,sys,urllib.request
from datetime import datetime,timezone
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent));from score import score
ROOT=Path(__file__).resolve().parents[1];body=os.environ.get("ISSUE_BODY","");user=os.environ.get("ISSUE_USER","unknown");num=os.environ.get("ISSUE_NUMBER","0")
def field(name):
    m=re.search(r"###\s*"+re.escape(name)+r"\s*\n+(.*?)(?=\n###\s|\Z)",body,re.S);v=(m.group(1).strip() if m else "");return "" if v=="_No response_" else v
URL=re.compile(r"https://github\.com/(?:user-attachments/files|[\w.-]+/[\w.-]+/files)/[^\s)\]]+")
def fetch(text):
    for u in URL.findall(text or ""):
        req=urllib.request.Request(u,headers={"User-Agent":"wbslink-bot"});data=urllib.request.urlopen(req,timeout=30).read(5_000_001)
        if len(data)>5_000_000:raise ValueError("File larger than 5 MB")
        return data.decode("utf-8-sig",errors="replace")
    return None
out=ROOT/"result.md"
try:
    which="practice" if "practice" in field("Which set?").lower() else "holdout"
    led=ROOT/"docs/data/ledger.json";ledger=json.loads(led.read_text(encoding="utf-8") or "[]") if led.exists() else []
    if which=="holdout" and any(e.get("user")==user and e.get("set")=="holdout" for e in ledger):
        out.write_text("### Challenge attempt not scored\n\nThe hidden challenge set allows one scored attempt per GitHub user. This protects the holdout answers from iterative probing. You can use the public practice set as often as you like.\n",encoding="utf-8");raise SystemExit(0)
    answers=fetch(field("Answers file"))
    if not answers:raise ValueError("No CSV attachment found in 'Answers file'. Drag your .csv file into that box so GitHub turns it into a link.")
    exc=fetch(field("Exceptions file (optional)"));r=score(answers,which,exc)
    try:minutes=float(re.findall(r"[\d.]+",field("Minutes spent"))[0])
    except (IndexError,ValueError):minutes=None
    entry={"issue":int(num),"user":user,"display_name":field("Display name")[:40] or user,"role":field("Your role (optional)"),"tools":field("Tools used"),"minutes":minutes,"submitted_utc":datetime.now(timezone.utc).isoformat(timespec="seconds"),**r};ledger.append(entry);led.write_text(json.dumps(ledger,indent=1),encoding="utf-8")
    best={}
    for e in ledger:
        k=(e["user"],e["set"]);rank=(e["silent_errors"],-e["correct"],-e["precision"],-e["coverage"],e["minutes"] if e["minutes"] is not None else 1e9)
        if k not in best or rank<best[k][0]:best[k]=(rank,e)
    board=sorted((v[1] for v in best.values()),key=lambda e:(e["set"],e["silent_errors"],-e["correct"],-e["precision"],-e["coverage"],e["minutes"] or 1e9));(ROOT/"docs/data/leaderboard.json").write_text(json.dumps(board,indent=1),encoding="utf-8")
    lines=[f"### Your WBS↔LINK Challenge score ({'Practice' if which=='practice' else 'Challenge'} set)","","| Measure | Result |","|---|---|",f"| **Silent errors** (confident wrong answers) | **{r['silent_errors']}** |",f"| Correct answers | {r['correct']} |",f"| Precision | {r['precision']:.1%} |",f"| Coverage | {r['coverage']:.1%} ({r['correct']+r['wrong']} of {r['records']} scored records answered) |"]
    if which=="practice":lines += [f"| Correct / wrong / unsure | {r['correct']} / {r['wrong']} / {r['unsure_or_blank']} |"]
    if "duplicate_ids_found" in r:lines += [f"| Duplicate/blank IDs flagged | {r['duplicate_ids_found']} |",f"| Structural changes flagged | {r['structural_changes_found']} |"]
    if minutes is not None:lines += [f"| Minutes (self-reported) | {minutes:.0f} |"]
    if r["matched_rows"]<0.5*r["records"]:lines += ["","⚠️ Fewer than half of your rows matched a scored record. Check `period`, `source_file` and `record_id` against the challenge rules."]
    if which=="holdout":lines += ["","The hidden challenge set allows one scored attempt per GitHub user. Detailed correct/wrong counts are not returned for the holdout."]
    lines += ["","Thank you for taking part. The leaderboard updates within a few minutes. Test product, synthetic data: see DISCLAIMER.md."];out.write_text("\n".join(lines),encoding="utf-8")
except SystemExit:pass
except Exception as e:
    out.write_text(f"### We couldn't score this submission\n\n{e}\n\nFor the hidden challenge set, scoring runs only when the issue is first opened. Check the public practice set and instructions before creating a new submission. Test product: see DISCLAIMER.md.",encoding="utf-8");sys.exit(0)
