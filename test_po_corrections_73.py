"""Product Owner defect checks supplement every existing commercial regression."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent / 'docs'
html = (ROOT / 'index.html').read_text()
css = (ROOT / 'site.css').read_text()
js = (ROOT / 'media-controls.js').read_text()

assert 'owner-wbs-integration.svg' in html
svg = (ROOT / 'assets/flagship/owner-wbs-integration.svg').read_text()
for required in ['OWNER', 'WBS', 'Schedule', 'Cost / forecast', 'Package / contract', 'evidence still required']:
    assert required in svg, required
# Hosted contract6135055002 replaces ambiguous dashed/merged routing.
assert svg.count('class="source-connection"') == 3
assert 'stroke-dasharray' not in svg and '<marker' not in svg
assert '.proof-grid img{aspect-ratio:auto;object-fit:contain;height:auto}' in css
assert html.count('aria-label="Open chart ') == 4
for name in ['executive-briefing-cycle2.png', 'premium-executive-view.png']:
    assert f'href="assets/flagship/{name}"' in html
assert 'proof-reading' in html
assert html.count('class="btn sound-play"') == 2
assert 'video.muted = false' in js and 'video.volume = 1' in js
for video in re.findall(r'<video\b[^>]*>', html):
    assert 'controls' in video and 'playsinline' in video
    assert 'autoplay' not in video and 'muted' not in video
assert 'wbslink-video-2-harbourlink.vtt' in html
vtt = (ROOT / 'videos/wbslink-video-2-harbourlink.vtt').read_text()
assert vtt.startswith('WEBVTT') and vtt.count('-->') == 10
assert 'Software interpretation does not approve a professional decision.' in vtt
assert 'No automatic approval is demonstrated or implied.' in vtt

def video_stream(path):
    return hashlib.sha256(subprocess.check_output([
        'ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:v:0', '-c', 'copy', '-f', 'h264', '-'
    ])).hexdigest()

assert video_stream(ROOT/'videos/wbslink-video-1-challenge.mp4') == video_stream(ROOT/'videos/source/wbslink-video-1-original.mp4')
for name in ['wbslink-video-1-challenge.mp4', 'wbslink-video-2-how-it-works.mp4']:
    p=ROOT/'videos'/name
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
    assert {s['codec_type'] for s in info['streams']} >= {'video','audio'}
    assert any(s['codec_name']=='aac' for s in info['streams'])
    assert any(s['codec_name']=='h264' and s['pix_fmt']=='yuv420p' for s in info['streams'])
    result=subprocess.run(['ffmpeg','-hide_banner','-i',str(p),'-af','volumedetect','-vn','-sn','-f','null','-'],capture_output=True,text=True,check=True).stderr
    mean=float(re.search(r'mean_volume: ([-.\d]+) dB',result)[1])
    peak=float(re.search(r'max_volume: ([-.\d]+) dB',result)[1])
    assert -30 < mean < -12, (name,mean)
    assert -25 < peak <= -1, (name,peak)

manifest=json.loads((ROOT/'videos/source/PO_CORRECTIONS_PROVENANCE.json').read_text())
for name,expected in manifest['files'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,name
print('Product Owner correction checks: PASS (original footage, evidence, captions, actual encoded audio)')
