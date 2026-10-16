"""Canonical data, editorial roles and navigation regressions for issue73."""
import importlib.util
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).parent
spec = importlib.util.spec_from_file_location('answer_charts', ROOT/'scripts/build_answer_led_charts_73.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class Figures(HTMLParser):
    def __init__(self):
        super().__init__(); self.figures=[]; self.current=None; self.details=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='details': self.details+=1
        if tag=='figure' and 'data-chart' in a:
            self.current={'number':int(a['data-chart']),'optional':self.details>0,'links':[],'classes':[],'text':''}; self.figures.append(self.current)
        if self.current:
            self.current['classes'] += a.get('class','').split()
            if tag=='a': self.current['links'].append(a.get('href'))
    def handle_endtag(self, tag):
        if tag=='figure':self.current=None
        if tag=='details':self.details-=1
    def handle_data(self,data):
        if self.current:self.current['text']+=data

html=(ROOT/'docs/index.html').read_text()
parsed=Figures();parsed.feed(html)
assert [f['number'] for f in parsed.figures]==[1,2,3,4]
assert [f['optional'] for f in parsed.figures]==[False,True,True,True]
for f in parsed.figures:
    for role in ['chart-question','chart-denominator','chart-meaning','chart-limit','chart-next']:
        assert role in f['classes'],(f['number'],role)
    next_link=f['links'][0]
    path,anchor=next_link.split('#')
    report=(ROOT/'docs'/path).read_text()
    assert f'id="{anchor}"' in report or f"id='{anchor}'" in report,(f['number'],next_link)
    assert 'What this means.' in f['text'] and 'What it does not mean.' in f['text']
assert 'WBS 1.5' in parsed.figures[0]['text'] and 'WBS 1.6' in parsed.figures[0]['text']
assert 'risk severity' in parsed.figures[1]['text']
assert 'Separate zero-based detail scale' in parsed.figures[2]['text']
assert 'missing work package or financial loss' in parsed.figures[3]['text']

# Deliberately different synthetic counts prove rendering is canonical, not pinned targets.
model={
 'coverage':{'numerator':1,'total':2,'branches':[{'code':'A','name':'Alpha','schedule':2,'cost':3},{'code':'B','name':'Beta','schedule':1,'cost':0}]},
 'source':{'rows':[['Source X',4,0,7],['Source Y',2,1,3]],'total':17},
 'movement':{'rows':[['Carried forward',8],['Re-keyed, revalidated',2],['Changed, re-decided',3],['New',1],['Retired',2]],'total':16},
 'outcomes':{'rows':[['Left unresolved on purpose (UNSURE)',10],['Scope not in the approved WBS (NEW_SCOPE)',0],['No WBS element applies (NO_WBS)',1]],'total':17}}
rendered=module.render(model)
assert '1 of 2 work areas' in rendered and '10 unresolved relationships' in rendered
assert '6 changed, new or retired' in rendered and '10 <small>of 16</small>' in rendered
assert 'WBS B Beta: missing cost relationships' in rendered
assert 'Contractor Programme' not in rendered
assert '264' not in rendered and '1,622' not in rendered and '1,613' not in rendered
assert 'width:100.000000%' in rendered and 'width:42.857143%' in rendered
print('answer-led-charts: PASS')
