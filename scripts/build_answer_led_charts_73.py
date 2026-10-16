"""Render website figures from the canonical approved report model, never invented counts.

Usage: python scripts/build_answer_led_charts_73.py --model PATH [--site docs]
Native-workbook PNGs remain labelled as separate native chart evidence.
"""
import argparse
import html
import json
from pathlib import Path

BEGIN = '<!-- ANSWER-LED FIGURES START -->'
END = '<!-- ANSWER-LED FIGURES END -->'
REPORT = 'examples/harbourlink/cycle2/Integrated_Management_Report.html'


def esc(v):
    return html.escape(str(v), quote=True)


def caption(number, denominator, meaning, limit, anchor, action):
    return (f'<figcaption><p class="chart-denominator">{esc(denominator)} '
            'Source: approved HarbourLink Cycle 2 report and Premium Workbook source tables.</p>'
            f'<p class="chart-meaning"><strong>What this means.</strong> {esc(meaning)}</p>'
            f'<p class="chart-limit"><strong>What it does not mean.</strong> {esc(limit)}</p>'
            f'<a class="chart-next" href="{REPORT}#{anchor}">Next: {esc(action)} →</a>'
            f'<a class="native-chart-route" href="assets/flagship/chart{number}.png" target="_blank" '
            f'rel="noopener" aria-label="Open chart {number} full size">Inspect original native workbook chart</a></figcaption>')


def figure(number, question, title, visual, explanation):
    return (f'<figure class="web-chart answer-led" id="website-figure-{number}" data-chart="{number}">'
            f'<p class="chart-question">{esc(question)}</p><h4>Figure {number:02d} | {esc(title)}</h4>'
            f'{visual}{explanation}</figure>')


def bars(rows):
    maximum = max((n for _, n in rows), default=0) or 1
    return '<div class="answer-bars">' + ''.join(
        f'<div class="answer-bar-row"><span>{esc(label)}</span><strong>{n:,}</strong>'
        f'<span class="answer-bar-track" aria-hidden="true"><span style="width:{n / maximum * 100:.6f}%"></span></span></div>'
        for label, n in rows) + '</div>'


def render(model):
    coverage, source, movement, outcomes = (model[k] for k in ('coverage', 'source', 'movement', 'outcomes'))
    branches = coverage['branches']
    table = '<table class="answer-coverage"><caption>Schedule and cost relationships through the Owner WBS</caption><thead><tr><th scope="col">Work area</th><th scope="col">Schedule</th><th scope="col">Cost</th></tr></thead><tbody>'
    for b in branches:
        table += f'<tr><th scope="row"><span>WBS {esc(b["code"])}</span>{esc(b["name"])}</th>'
        for role in ('schedule', 'cost'):
            present = b[role] > 0
            table += f'<td class="{("present" if present else "absent")}">{("Present" if present else "Absent")}</td>'
        table += '</tr>'
    table += '</tbody></table>'
    gaps = '; '.join(f'WBS {b["code"]} {b["name"]}: missing {role} relationships'
                     for b in branches for role in ('schedule', 'cost') if b[role] == 0)
    f1 = figure(1, 'Which parts of my project are missing a schedule or cost connection?',
                f'{coverage["numerator"]} of {coverage["total"]} work areas have both connections.', table,
                caption(1, f'{coverage["total"]} reported Owner-WBS branches.', gaps + '.',
                        'Coverage is not project progress or health, or direct schedule-to-cost equivalence.',
                        'S02', 'inspect the two gaps and exact governed Action'))
    unresolved = sorted([(r[0], r[3]) for r in source['rows']], key=lambda r: -r[1])
    # Source assertions retain supplied names; controlled Canadian copy is secondary.
    visual2 = bars([(name if name != 'Contractor Programme' else 'Contractor Program', n) for name, n in unresolved])
    if any(name == 'Contractor Programme' for name, _ in unresolved):
        visual2 += '<p class="source-name-note">Source name as supplied: Contractor Programme</p>'
    total = sum(n for _, n in unresolved)
    f2 = figure(2, 'Where should our controls team look first for unresolved relationships?',
                f'{total:,} unresolved relationships show where evidence review is needed.', visual2,
                caption(2, f'{total:,} current unresolved within {source["total"]:,} current relationships; retired excluded; split targets counted once.',
                        'The counts locate the unresolved review workload by source.',
                        'These counts do not establish cause or risk severity; no relationship is auto-assigned.',
                        'S03', 'follow unresolved records to Crosswalk and Evidence'))
    values = dict(movement['rows'])
    carried, revalidated = values.get('Carried forward', 0), values.get('Re-keyed, revalidated', 0)
    details = [(name, values.get(name, 0)) for name in ('Changed, re-decided', 'New', 'Retired')]
    detail_total = sum(n for _, n in details)
    visual3 = (f'<div class="movement-panels"><section><h5>Stable or revalidated</h5><p class="answer-metric">{carried + revalidated:,} <small>of {movement["total"]:,}</small></p>'
               f'<p>{carried:,} carried forward<br>{revalidated:,} re-keyed, revalidated</p></section>'
               f'<section><h5>Movement detail · {detail_total:,} relationships</h5>{bars(details)}'
               '<p class="scale-note">Separate zero-based detail scale. Stable and revalidated relationships excluded.</p></section></div>')
    f3 = figure(3, 'What changed since the last approved report?',
                f'{detail_total:,} changed, new or retired relationships deserve a closer look.', visual3,
                caption(3, f'{movement["total"]:,} relationships including retired; {carried + revalidated:,} remained valid.',
                        'Carry-forward and revalidation remain distinct; the detail makes the smaller changes readable.',
                        'The movement denominator includes retired relationships, unlike current relationship counts.',
                        'S04', 'inspect changed, new and retired records and revision evidence'))
    statuses = ['UNSURE', 'NEW_SCOPE', 'NO_WBS']
    definitions = ['Evidence does not support an assigned relationship yet.', 'Recorded as scope not in the approved WBS.', 'Recorded as having no applicable WBS element.']
    cards = '<div class="outcome-cards">' + ''.join(
        f'<section><h5>{status}</h5><strong>{n:,}</strong><p>{esc(label)}</p><p>{definition}</p></section>'
        for (label, n), status, definition in zip(outcomes['rows'], statuses, definitions)) + '</div>'
    f4 = figure(4, 'Does an unresolved link mean missing work?', 'No. Uncertainty and outside-WBS outcomes are different decisions.', cards,
                caption(4, f'{outcomes["total"]:,} current relationships; retired excluded.',
                        'Unresolved records need evidence review. NEW_SCOPE and NO_WBS retain their separate governed meanings.',
                        'An unresolved relationship does not establish a missing work package or financial loss.',
                        'S05', 'review unresolved evidence and the bounded professional decision'))
    return (BEGIN + '\n<div class="primary-coverage-figure">' + f1 + '</div>\n'
            '<details class="analytical-details"><summary>For project-controls teams: inspect unresolved records and cycle changes</summary>'
            '<div class="analytics-proof"><p class="eyebrow">OPTIONAL PROFESSIONAL ANALYSIS</p>'
            '<div class="chart-proof-grid">' + f2 + f3 + f4 + '</div></div></details>\n' + END)


def update(site, model):
    p = site / 'index.html'
    text = p.read_text()
    if BEGIN in text:
        start, end = text.index(BEGIN), text.index(END) + len(END)
    else:
        start = text.index('  <details class="analytical-details">')
        end = text.index('</details>', start) + len('</details>')
    p.write_text(text[:start] + render(model) + text[end:])


if __name__ == '__main__':
    cli = argparse.ArgumentParser()
    cli.add_argument('--model', type=Path, required=True)
    cli.add_argument('--site', type=Path, default=Path('docs'))
    args = cli.parse_args()
    update(args.site, json.loads(args.model.read_text()))
