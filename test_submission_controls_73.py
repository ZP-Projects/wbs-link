"""Offline submission lifecycle checks; no live challenge or attachment requests."""
import importlib.util
import io
import json
import runpy
import sys
import types
from pathlib import Path

import pytest

SCORER = Path(__file__).parent / 'scorer'
sys.path.insert(0, str(SCORER))
from public_results import public_entry
from reserve_attempt import reserve

BODY = '### Which set?\n{which}\n### Answers file\nhttps://github.com/user-attachments/files/123/synthetic.csv'
RESULT = {'set': 'holdout', 'records': 12, 'correct': 7, 'wrong': 2,
          'silent_errors': 1, 'unsure_or_blank': 3, 'net_score': 1.5,
          'precision': .7778, 'coverage': .75, 'matched_rows': 9,
          'future_private_counter': 42}


@pytest.fixture
def root(tmp_path):
    (tmp_path / 'scorer').mkdir()
    (tmp_path / 'scorer/score_issue.py').write_text((SCORER / 'score_issue.py').read_text())
    (tmp_path / 'docs/data').mkdir(parents=True)
    for name in ['ledger', 'leaderboard']:
        (tmp_path / f'docs/data/{name}.json').write_text('[]')
    return tmp_path


def execute(root, monkeypatch, which='holdout', fail=False):
    calls = []
    fake = types.ModuleType('score')
    def score(*args):
        calls.append(args)
        if fail:
            raise ValueError('synthetic scoring failure')
        return dict(RESULT, set=which)
    fake.score = score
    monkeypatch.setitem(sys.modules, 'score', fake)
    monkeypatch.setattr('urllib.request.urlopen', lambda *a, **k: io.BytesIO(b'synthetic CSV'))
    for key, value in dict(ISSUE_BODY=BODY.format(which=which), ISSUE_USER='synthetic-reviewer',
                           ISSUE_NUMBER='999', REQUIRE_HOLDOUT_RESERVATION='1').items():
        monkeypatch.setenv(key, value)
    try:
        runpy.run_path(str(root / 'scorer/score_issue.py'))
    except SystemExit as exc:
        assert exc.code == 0
    return calls


def test_hidden_projection_is_allowlist():
    entry = public_entry(dict(RESULT, user='reviewer', issue=1))
    assert entry['net_score'] == RESULT['net_score']
    assert entry['precision'] == RESULT['precision']
    assert not set(['correct', 'wrong', 'unsure_or_blank', 'records', 'matched_rows', 'future_private_counter']) & entry.keys()


def test_success_requires_persisted_reservation_and_keeps_details_private(root, monkeypatch):
    persisted = []
    def persist(path):
        persisted.append(json.loads((path / 'docs/data/ledger.json').read_text()))
    assert reserve(root, 'synthetic-reviewer', '999', BODY.format(which='holdout'), persist)
    assert persisted[0][0]['status'] == 'reserved'
    assert execute(root, monkeypatch)
    for filename in ['ledger', 'leaderboard']:
        entries = json.loads((root / f'docs/data/{filename}.json').read_text())
        assert entries[0]['status'] == 'scored'
        assert not set(['correct', 'wrong', 'unsure_or_blank', 'records', 'matched_rows', 'future_private_counter']) & entries[0].keys()
    assert 'Detailed reference-match counts are not returned' in (root / 'result.md').read_text()
    assert not reserve(root, 'synthetic-reviewer', '1000', BODY.format(which='holdout'), lambda _: pytest.fail('must not persist again'))


def test_failed_scoring_keeps_attempt_reserved(root, monkeypatch):
    reserve(root, 'synthetic-reviewer', '999', BODY.format(which='holdout'), lambda _: None)
    assert execute(root, monkeypatch, fail=True)
    assert json.loads((root / 'docs/data/ledger.json').read_text())[0]['status'] == 'reserved'
    assert not reserve(root, 'synthetic-reviewer', '1000', BODY.format(which='holdout'), lambda _: None)


def test_reservation_push_failure_never_grants_eligibility(root):
    def fail(_):
        raise RuntimeError('synthetic persistence failure')
    with pytest.raises(RuntimeError):
        reserve(root, 'synthetic-reviewer', '999', BODY.format(which='holdout'), fail)


def test_unreserved_holdout_never_calls_scorer(root, monkeypatch):
    assert not execute(root, monkeypatch)


def test_practice_preserves_legitimate_feedback(root, monkeypatch):
    assert reserve(root, 'synthetic-reviewer', '999', BODY.format(which='practice'), lambda _: pytest.fail('practice needs no reservation'))
    assert execute(root, monkeypatch, which='practice')
    entry = json.loads((root / 'docs/data/ledger.json').read_text())[0]
    assert entry['correct'] == 7 and entry['matched_rows'] == 9
    assert 'future_private_counter' not in entry
    assert 'Matches reference / differs / unresolved | 7 / 2 / 3' in (root / 'result.md').read_text()


def test_workflow_serializes_and_reserves_before_scoring():
    text = (SCORER.parent / '.github/workflows/score.yml').read_text()
    assert 'group: "challenge-scoring"' in text
    assert text.index('git pull --ff-only') < text.index('python scorer/reserve_attempt.py') < text.index('python scorer/score_issue.py')
    assert 'REQUIRE_HOLDOUT_RESERVATION: "1"' in text
