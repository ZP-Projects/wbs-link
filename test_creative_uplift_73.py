"""Frozen v4 creative contract, preserved in full; current v5 has separate production tests."""
from pathlib import Path
import hashlib,json,subprocess,re
DOCS=Path(__file__).parent/'docs';D=DOCS/'archive/full-suite-production-v4';V=D/'videos';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def stream(p,kind,format):return subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map',f'0:{kind}:0','-c','copy','-f',format,'-'])
def test_current_reports_preserve_all_accepted_governed_model_fields():
 for c in [1,2]:
  m=json.loads((D/f'examples/harbourlink/cycle{c}/report-content.json').read_text())
  old=json.loads(subprocess.check_output(['git','show',f'd3cf7690913cf7cda33ef029fa3be505cf080549:docs/examples/harbourlink/cycle{c}/report-content.json']))
  assert m['presentation_edition']=='creative-uplift-2026-v4'
  for x in [m,old]:
   for k in ['presentation_edition','content_sha256']:x.pop(k)
  assert m==old
  assert (D/f'examples/harbourlink/cycle{c}/Premium_Workbook.xlsx').read_bytes()==(DOCS/f'archive/creative-uplift-baseline/examples/harbourlink/cycle{c}/Premium_Workbook.xlsx').read_bytes()
 data=json.loads((D/'assets/flagship/chart-data.json').read_text());assert data['presentation_edition']=='creative-uplift-2026-v4' and data['charts'][0]['values_by_series']==[[4,1,1,0]] and data['charts'][2]['values_by_series']==[[1613,1,4,4,3]]
def test_actual_report_components_have_source_and_pixel_custody():
 p=json.loads((V/'source/CREATIVE_UPLIFT_73_PROVENANCE.json').read_text());assert len(p['proof'])==24
 for x in p['proof']:
  assert x['source_sha256']==sha(D/'examples/harbourlink'/x['source'])
  assert x['sha256']==sha(V/'source/creative-proof'/x['image'])
 assert len(set(x['image_sha256'] for x in p['film1']['scenes']))==10
 assert '81 records' in next(x['component_text'] for x in p['proof'] if 'bounded-decision' in x['image'])
def test_full_current_compositions_captions_and_original_film2_audio():
 for name,vtt,seconds,cues in [('wbslink-video-1-challenge.mp4','wbslink-video-1-cinematic.vtt',60,10),('wbslink-video-2-how-it-works.mp4','wbslink-video-2-harbourlink.vtt',80,10),('wbslink-video-2-how-it-works-phone.mp4','wbslink-video-2-how-it-works-phone.vtt',80,10)]:
  info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(V/name)]));assert abs(float(info['format']['duration'])-seconds)<.1
  assert {s['codec_name'] for s in info['streams']}>={'h264','aac'}
  text=(V/vtt).read_text();assert text.startswith('WEBVTT') and text.count('-->')==cues
  assert f'00:01:{seconds-60:02d}.000' in text
  assert 'Confirm whether the missing governed relationship is expected or requires project-controls attention.' in text
  subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(V/name),'-f','null','-'],check=True)
  if 'video-2' in name:
   assert hashlib.sha256(stream(V/name,'a','adts')).hexdigest()=='efbc20c98b93cc5681299e910eeb58e74e834b070685facb8472f28ca2ee88de'
 assert stream(V/'wbslink-video-1-challenge.mp4','v','h264')!=stream(DOCS/'archive/creative-uplift-baseline/videos/wbslink-video-1-challenge.mp4','v','h264')
def test_commercial_and_audio_copy_matches_new_cut_without_false_live_parity():
 h=(D/'index.html').read_text();assert 'Original custom graphics and actual HarbourLink report evidence' in h
 assert 'picture-matched workplace and equipment sounds' not in h
 assert 'no spoken narration' in h.lower() and 'Use synthetic practice data only' in h
 p=json.loads((V/'source/PO_CORRECTIONS_PROVENANCE.json').read_text());assert p['hosted_parity'].startswith('NOT VERIFIED')
 for name,digest in p['files'].items():assert sha(D/name)==digest,name
