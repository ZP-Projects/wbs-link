from pathlib import Path
import re, zipfile, subprocess, json
ROOT=Path(__file__).parent/'docs'
html=(ROOT/'index.html').read_text(encoding='utf-8')
low=html.lower()

order=['id="top"','id="video1"','id="spine"','id="why"','id="video2"','id="proof"','id="cycle2"','id="practice"','id="pilot"','id="community"']
pos=[low.index(x) for x in order]
assert pos==sorted(pos), pos
assert low.index('id="practice"') < low.index('id="community"')

for forbidden in ['single source of truth','production ready','production-ready','canadian-hosted','guaranteed savings','delay prevention','% faster','times faster']:
    assert forbidden not in low, forbidden
for required in ['owner wbs','integration spine','preserve uncertainty','professional authority','reporting cycle','practice project']:
    assert required in low, required

attrs=re.findall(r'(?:href|src)="([^"]+)"',html)
for ref in attrs:
    if ref.startswith(('http://','https://','#','mailto:')): continue
    p=(ROOT/ref.split('#')[0]).resolve()
    assert p.exists(), f'missing {ref}'

for tag in re.findall(r'<img\b[^>]*>',html,re.I): assert 'alt=' in tag.lower(), tag
for tag in re.findall(r'<video\b[^>]*>',html,re.I): assert 'aria-label=' in tag.lower(), tag

z=ROOT/'downloads/harbourlink-practice-project.zip'
with zipfile.ZipFile(z) as zf:
    names='\n'.join(zf.namelist()).lower()
    for bad in ['truth_package','oracle','expected_conditions','answer_key','reference_mapping']:
        assert bad not in names, bad
    assert 'cycle1/' in names and 'cycle2/' in names and 'case_briefing.md' in names and 'mission_guide.md' in names

for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.json','.csv','.xlsx'}:
        assert 'truth' not in p.name.lower() and 'oracle' not in p.name.lower(), p

for name,lo_d,hi_d in [('wbslink-video-1-challenge.mp4',55,95),('wbslink-video-2-how-it-works.mp4',65,105)]:
    p=ROOT/'videos'/name
    out=subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(p)],text=True)
    dur=float(json.loads(out)['format']['duration'])
    assert lo_d <= dur <= hi_d,(name,dur)

print('commercial-static-checks: PASS')
