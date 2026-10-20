"""Actual current production files, separate from retained historical creative tests."""
from pathlib import Path
import json,hashlib,re,subprocess,io
from PIL import Image,ImageChops,ImageStat
D=Path(__file__).parent/'docs';V=D/'videos';S=V/'source/full_suite_production_73'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def test_current_sealed_models_preserve_entire_accepted_professional_record():
 for c in [1,2]:
  old=json.loads((D/f'archive/full-suite-production-v4/examples/harbourlink/cycle{c}/report-content.json').read_text());new=json.loads((D/f'examples/harbourlink/cycle{c}/report-content.json').read_text());assert new['presentation_edition']=='full-suite-production-2026-v5'
  for m in [old,new]:
   for k in ['presentation_edition','content_sha256']:m.pop(k)
  assert old==new
  assert sha(D/f'examples/harbourlink/cycle{c}/Premium_Workbook.xlsx')==sha(D/f'archive/full-suite-production-v4/examples/harbourlink/cycle{c}/Premium_Workbook.xlsx')
def test_all_complete_compositions_have_picture_sound_and_full_matching_captions():
 films=[('1-challenge','1-cinematic',60,8,1920,1080),('1-challenge-phone','1-challenge-phone',60,8,1080,1920),('2-how-it-works','2-harbourlink',80,10,1920,1080),('2-how-it-works-phone','2-how-it-works-phone',80,10,1080,1920)]
 for f,c,t,n,w,h in films:
  p=V/f'wbslink-video-{f}.mp4';j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));assert abs(float(j['format']['duration'])-t)<.1
  a=next(s for s in j['streams'] if s['codec_type']=='audio');v=next(s for s in j['streams'] if s['codec_type']=='video');assert a['codec_name']=='aac' and (v['width'],v['height'])==(w,h) and v['codec_name']=='h264'
  cap=(V/f'wbslink-video-{c}.vtt').read_text();times=re.findall(r'(\d\d:\d\d:\d\d\.\d{3}) --> (\d\d:\d\d:\d\d\.\d{3})',cap);assert len(times)==n
  assert times[0][0]=='00:00:00.000' and times[-1][1]==f'00:01:{t-60:02d}.000'
  assert cap.count('-->')==n
  if f.startswith('1-'):
   assert 'payment' in cap.lower() and 'Owner WBS' in cap and 'Confirm whether the missing governed relationship is expected or requires project-controls attention.' in cap
  else:
   assert 'Software interpretation does not approve a professional decision.' in cap and 'No automatic approval is demonstrated or implied.' in cap
 def packets(p):return subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','adts','-'])
 assert hashlib.sha256(packets(V/'wbslink-video-2-how-it-works.mp4')).hexdigest()=='efbc20c98b93cc5681299e910eeb58e74e834b070685facb8472f28ca2ee88de'
 assert packets(V/'wbslink-video-2-how-it-works.mp4')==packets(V/'wbslink-video-2-how-it-works-phone.mp4')
def test_original_capture_and_cinematic_art_custody():
 rows=json.loads((S/'report-captures/PROVENANCE.json').read_text());assert len(rows)==24
 for x in rows:
  assert x['source_sha256']==sha(D/'examples/harbourlink/cycle2/Integrated_Management_Report.html') and x['sha256']==sha(S/'report-captures'/x['image'])
 a=json.loads((S/'ART_PROVENANCE.json').read_text());assert len(a['assets'])==3 and not a['third_party_stock']
 assert len({x['sha256'] for x in a['assets']})==3
 for x in a['assets']:assert x['sha256']==sha(S/x['file']) and 'fictional' in x['provenance']
 p=json.loads((S/'PROVENANCE.json').read_text());assert p['edition']=='full-suite-production-2026-v5'
 for n,h in p['files'].items():assert sha(D/n)==h,n
def test_film1_middle_has_actual_temporal_motion_in_each_distinct_sequence():
 def frame(t,phone):
  n='wbslink-video-1-challenge'+('-phone' if phone else '')+'.mp4'
  data=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(V/n),'-frames:v','1','-vf','scale=480:-1','-f','image2pipe','-vcodec','png','-']);return Image.open(io.BytesIO(data)).convert('RGB')
 for phone in [False,True]:
  for a,b in [(20.2,24.5),(28,34.8),(36.6,40),(44.1,48)]:
   diff=ImageStat.Stat(ImageChops.difference(frame(a,phone),frame(b,phone))).mean;assert sum(diff)>0.15,(phone,a,b,diff)
def test_phone_movie_and_caption_sources_are_paired_and_accessible():
 h=(D/'index.html').read_text();js=(D/'media-controls.js').read_text()
 for n in ['1-challenge','2-how-it-works']:
  assert f'data-phone-src="videos/wbslink-video-{n}-phone.mp4"' in h and f'data-phone-captions="videos/wbslink-video-{n}-phone.vtt"' in h
 assert 'video.dataset.phoneCaptions' in js and "track.mode = 'showing'" in js
 assert 'video.muted = false' in js and 'if (video.volume === 0)' in js
 assert 'autoplay' not in re.sub(r'<!--.*?-->','',h,flags=re.S).lower()
