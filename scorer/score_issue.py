"""Submission bot: reads a GitHub issue created from the 'Submit results' form, downloads the attached CSVs, scores them,
writes result.md (posted as a comment) and appends to docs/data/ledger.json and docs/data/leaderboard.json.
Security: the issue body is read from an environment variable and treated as data; only GitHub attachment URLs are fetched."""
import json, os, re, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from score import score

ROOT = Path(__file__).resolve().parents[1]
body = os.environ.get("ISSUE_BODY", ""); user = os.environ.get("ISSUE_USER", "unknown"); num = os.environ.get("ISSUE_NUMBER", "0")


def field(name):
    m = re.search(r"###\s*" + re.escape(name) + r"\s*\n+(.*?)(?=\n###\s|\Z)", body, re.S)
    v = (m.group(1).strip() if m else "")
    return "" if v == "_No response_" else v


URL = re.compile(r"https://github\.com/(?:user-attachments/files|[\w.-]+/[\w.-]+/files)/[^\s)\]]+")


def fetch(text):
    for u in URL.findall(text or ""):
        req = urllib.request.Request(u, headers={"User-Agent": "wbslink-bot"})
        data = urllib.request.urlopen(req, timeout=30).read(5_000_001)
        if len(data) > 5_000_000:
            raise ValueError("File larger than 5 MB")
        return data.decode("utf-8-sig", errors="replace")
    return None


out = ROOT / "result.md"
try:
    which = "practice" if "practice" in field("Which set?").lower() else "holdout"
    answers = fetch(field("Answers file"))
    if not answers:
        raise ValueError("No CSV attachment found in 'Answers file'. Drag your .csv file into that box so GitHub turns it into a link.")
    exc = fetch(field("Exceptions file (optional)"))
    r = score(answers, which, exc)
    try:
        minutes = float(re.findall(r"[\d.]+", field("Minutes spent"))[0])
    except (IndexError, ValueError):
        minutes = None
    entry = {"issue": int(num), "user": user, "display_name": field("Display name")[:40] or user, "role": field("Your role (optional)"),
             "tools": field("Tools used"), "minutes": minutes, "submitted_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), **r}
    led = ROOT / "docs/data/ledger.json"; ledger = json.loads(led.read_text() or "[]") if led.exists() else []
    ledger.append(entry); led.write_text(json.dumps(ledger, indent=1))
    best = {}
    for e in ledger:
        k = (e["user"], e["set"])
        rank = (e["silent_errors"], -e["precision"], -e["coverage"], e["minutes"] if e["minutes"] is not None else 1e9)
        if k not in best or rank < best[k][0]:
            best[k] = (rank, e)
    board = sorted((v[1] for v in best.values()), key=lambda e: (e["set"], e["silent_errors"], -e["precision"], -e["coverage"], e["minutes"] or 1e9))
    (ROOT / "docs/data/leaderboard.json").write_text(json.dumps(board, indent=1))
    lines = [f"### Your WBS↔LINK Challenge score ({'Practice' if which == 'practice' else 'Challenge'} set)", "",
             "| Measure | Result |", "|---|---|",
             f"| **Silent errors** (confident wrong answers) | **{r['silent_errors']}** |",
             f"| Precision | {r['precision']:.1%} |", f"| Coverage | {r['coverage']:.1%} ({r['correct'] + r['wrong']} of {r['records']} records answered) |",
             f"| Correct / wrong / unsure | {r['correct']} / {r['wrong']} / {r['unsure_or_blank']} |"]
    if "duplicate_ids_found" in r:
        lines += [f"| Duplicate/blank IDs flagged | {r['duplicate_ids_found']} |", f"| Structural changes flagged | {r['structural_changes_found']} |"]
    if minutes is not None:
        lines += [f"| Minutes (self-reported) | {minutes:.0f} |"]
    if r["matched_rows"] < 0.5 * r["records"]:
        lines += ["", "⚠️ Fewer than half of your rows matched a record. Check the `period`, `source_file` and `record_id` columns against the template."]
    lines += ["", "Thank you for taking part. The leaderboard updates within a few minutes. Test product, synthetic data: see DISCLAIMER.md."]
    out.write_text("\n".join(lines))
except Exception as e:
    out.write_text(f"### We couldn't score this submission\n\n{e}\n\nEdit the issue to fix it and the bot will try again. Test product: see DISCLAIMER.md.")
    sys.exit(0)
