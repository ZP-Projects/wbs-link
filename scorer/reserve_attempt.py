"""Persist the holdout attempt before any scoring work is permitted."""
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from public_results import public_entry

ROOT = Path(__file__).resolve().parents[1]


def reserve(root, user, number, body, persist):
    ledger_path = root / 'docs/data/ledger.json'
    ledger = [public_entry(e) for e in json.loads(ledger_path.read_text() or '[]')]
    match = re.search(r'###\s*Which set\?\s*\n+(.*?)(?=\n###\s|\Z)', body, re.S)
    if match and 'practice' in match[1].lower():
        return True
    if any(e.get('user') == user and e.get('set') == 'holdout' for e in ledger):
        (root / 'result.md').write_text('### Challenge attempt not scored\n\nThe hidden challenge set allows one scored attempt per GitHub user.\n')
        return False
    ledger.append({'issue': int(number), 'user': user, 'set': 'holdout',
                   'status': 'reserved', 'submitted_utc': datetime.now(timezone.utc).isoformat(timespec='seconds')})
    ledger_path.write_text(json.dumps(ledger, indent=1))
    board_path = root / 'docs/data/leaderboard.json'
    board_path.write_text(json.dumps([public_entry(e) for e in json.loads(board_path.read_text() or '[]')], indent=1))
    persist(root)
    return True


def commit_reservation(root):
    for args in [ ['git', 'add', 'docs/data/ledger.json', 'docs/data/leaderboard.json'],
                  ['git', 'commit', '-m', 'Reserve challenge attempt'],
                  ['git', 'push'] ]:
        subprocess.run(args, cwd=root, check=True)


if __name__ == '__main__':
    eligible = reserve(ROOT, os.environ['ISSUE_USER'], os.environ['ISSUE_NUMBER'],
                       os.environ.get('ISSUE_BODY', ''), commit_reservation)
    with open(os.environ['GITHUB_OUTPUT'], 'a') as output:
        output.write(f"eligible={'true' if eligible else 'false'}\n")
