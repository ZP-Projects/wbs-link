from pathlib import Path
import re, zipfile, subprocess, json, hashlib
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
    streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type','-of','json',str(p)],text=True))['streams']
    kinds={stream['codec_type'] for stream in streams}
    assert {'video','audio'} <= kinds,(name,kinds)


# Community navigation and retired-claim regression gate (Coordinator #52).
community_targets = ['how-to.html', 'leaderboard.html', 'healthcheck.html']
community_section = html.split('id="community"', 1)[1].split('</section>', 1)[0]
community_links = re.findall(r'href="([^"]+)"', community_section)
assert community_links == ['how-to.html', 'how-to.html', 'leaderboard.html', 'healthcheck.html'], community_links
for target in community_targets:
    assert (ROOT / target).is_file(), target
    page = (ROOT / target).read_text(encoding='utf-8').lower()
    assert 'index.html#community' in page, target
    assert 'index.html#challenge' not in page, target
    for retired in ['early-stage concept', 'secure, ai-enabled',
                    'pressure-test the problem before pretending the product is finished',
                    'wbs↔link is a working product name', 'early beta']:
        assert retired not in page, (target, retired)
    assert 'synthetic' in page and 'never upload real project' in page, target
assert 'community challenge' in (ROOT / 'how-to.html').read_text(encoding='utf-8').lower()
checker = (ROOT / 'healthcheck.html').read_text(encoding='utf-8')
assert 'Stable identifiers can make month-to-month comparison easier.' in checker
assert 'Stable IDs make month-to-month mapping cheap.' not in checker
assert 'in your browser only' in checker


# Issue #3 visual-first commercial experience contract.
assert 'WBS↔LINK' in html and 'by ZP Synergy Group' in html
assert 'https://www.zpsynergygroup.ca/' in html
assert 'rel="noopener noreferrer"' in html
assert '<details class="more-detail">' in html
assert '<summary>' in html
assert html.count('class="visual-icon"') >= 4
assert 'href="#video1"' in html and 'href="#video2"' in html
assert 'id="practice"' in html and 'id="cycle2"' in html
assert 'id="community"' in html
assert 'videos/wbslink-video-1-challenge.mp4' in html
assert 'videos/wbslink-video-2-how-it-works.mp4' in html
for poster in ('wbslink-video-1-challenge.jpg', 'wbslink-video-2-how-it-works.jpg'):
    assert (ROOT / 'videos' / poster).is_file(), poster

if (ROOT / 'videos/wbslink-video-1-original-footage.lock').exists():
    manifest = json.loads((ROOT / 'videos/source/VIDEO1_ASSET_MANIFEST.json').read_text())
    for name, expected in manifest['assets'].items():
        assert hashlib.sha256((ROOT / 'videos' / name).read_bytes()).hexdigest() == expected, name
    assert '<track kind="captions" src="videos/wbslink-video-1-cinematic.vtt" srclang="en" label="English" default>' in html

print('commercial-static-checks: PASS')
