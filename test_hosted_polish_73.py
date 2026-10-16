"""Hosted contract6135055002: original media structure and approved-data display bounds."""
from pathlib import Path
import json,hashlib,subprocess,re,xml.etree.ElementTree as E
import numpy as np
R=Path(__file__).parent/'docs';html=(R/'index.html').read_text();svg=E.parse(R/'assets/flagship/owner-wbs-integration.svg').getroot();ns={'s':'http://www.w3.org/2000/svg'}
connections=svg.findall('.//s:path[@class="source-connection"]',ns);assert [p.attrib['d'] for p in connections]==['M66 160V236','M195 160V236','M324 160V236']
assert {p.attrib['data-source'] for p in connections}=={'schedule','cost','package'}
assert '<marker' not in (R/'assets/flagship/owner-wbs-integration.svg').read_text() and 'stroke-dasharray' not in (R/'assets/flagship/owner-wbs-integration.svg').read_text()
assert 'executive-briefing-cycle2.png" alt="Complete actual' in html
assert 'Confirm whether the missing governed relationship is expected or requires project-controls attention.' in html
cat=json.loads((R/'assets/flagship/display-terms.json').read_text());data=json.loads((R/'assets/flagship/chart-data.json').read_text());assert cat['version']==data['copy_version']=='en-CA/73.1'
# Independently retrieved through GitHub at immutable producer commit
# 4b9fbc4306a1b35ca2e606547dcfd1624cb05eae (blob2343031efc63edd6f692952a7cf84251ed82c2e2,
# 555129 bytes). This remains a fixed oracle, not a hash derived from the file under test.
assert data['governed_output_basis_sha']=='4b9fbc4306a1b35ca2e606547dcfd1624cb05eae'
assert data['source_product_sha']=='de958f0aa4f9ce8d71095a17f53a325361d49360'
assert data['current_scenario']=='harbourlink-reporting-2026-v2'
assert data['governed_baseline_workbook_sha256']=='728df9ac02d5fea0dbe8b7ff39fe918d9367fdd4a70f09f4e5cf72cbe120f088'
assert data['workbook_sha256']=='606bc80650f714a2229c942ddc377bf2ebfba599dbdf5aa3c60266801b45a782'
assert hashlib.sha256((R/'examples/harbourlink/cycle2/Premium_Workbook.xlsx').read_bytes()).hexdigest()=='606bc80650f714a2229c942ddc377bf2ebfba599dbdf5aa3c60266801b45a782'
assert data['charts'][0]['values_by_series']==[[4,1,1,0]] and data['charts'][2]['values_by_series']==[[1613,1,4,4,3]] and data['charts'][3]['values_by_series']==[[264,0,1]]
assert sum(sum(v) for v in data['charts'][1]['values_by_series'])==1622
for x in data['charts'][1]['source_categories']:
 if x=='Contractor Programme':assert 'Contractor Program' in data['charts'][1]['display_categories'] and 'Source name as supplied: Contractor Programme' in html
assert html.count('class="chart-denominator"')==4 and 'lang="en-CA"' in html
for number,seconds,cues in [(1,60,15),(2,80,10)]:
 name=f'wbslink-video-{number}-'+('challenge' if number==1 else 'how-it-works')+'.mp4';path=R/'videos'/name
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(path)]));assert abs(float(info['format']['duration'])-seconds)<.1
 assert {s['codec_name'] for s in info['streams']}>={'h264','aac'}
 vtt=(R/'videos'/('wbslink-video-1-cinematic.vtt' if number==1 else 'wbslink-video-2-harbourlink.vtt')).read_text();assert vtt.count('-->')==cues
 audio=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ar','16000','-ac','1','-f','f32le','-']),dtype='<f4');assert np.max(np.abs(audio))<.98
 rms=[float(np.sqrt(np.mean(a*a))) for a in np.array_split(audio,cues)];assert min(rms)>.002
 if number==1:
  f=np.fft.rfftfreq(len(audio),1/16000);energy=abs(np.fft.rfft(audio))**2;assert float(energy[(f>=250)&(f<=8000)].sum()/energy.sum())>.45
js=(R/'media-controls.js').read_text();assert 'if (video.volume === 0)' in js
print('Hosted contract checks: PASS;3independent connections, approved cell populations/labels, full60/80s encoding and audibility-band signal. No human listening claim.')
