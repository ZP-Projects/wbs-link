"""Refresh the preserved 10-scene cut with actual current UI and honest close-ups.

No approval transaction is performed. Uses the existing accepted recorded music
mix; no synthetic score and no isolated-guitar-stem claim.
"""
from pathlib import Path
import argparse,importlib.util,json,subprocess,shutil
from PIL import Image,ImageDraw,ImageFont
from playwright.sync_api import sync_playwright

HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--app-url',required=True);p.add_argument('--site-url',required=True);p.add_argument('--only-scenes',default='');p.add_argument('--preview-only',action='store_true');p.add_argument('--audio-track',type=Path);args=p.parse_args()
r=args.work;r.mkdir(parents=True,exist_ok=True);ui=HERE/'harbourlink_ui';details=r/'detail';details.mkdir(exist_ok=True)
metadata={'app_url':args.app_url,'source':'Actual local isolated candidate with approved fictional synthetic HarbourLink data','actions':[],'approval_performed':False,'timeline':'10 scenes, 8 seconds each, preserved sequence','closeups':'Complete actual elements; established interface precedes detail. No fabricated click or uninterrupted approval transaction.'}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium');page=b.new_page(viewport={'width':1600,'height':1000},device_scale_factor=3)
 for name,path in [('project','/p/1/overview'),('wbs','/p/1/explorer?node=WBS%3A1.5'),('evidence','/p/1/crosswalk?q=SCH-05-001'),('interpretation','/examples/harbourlink/cycle/2#S05'),('report','/examples/harbourlink/cycle/2#S01'),('charts','/p/1/deliverables'),('cycle2','/examples/harbourlink/cycle/2#S04'),('approval','/examples/harbourlink/cycle/2#S06'),('guide','/projects/harbourlink')]:
  page.set_viewport_size({'width':1600,'height':1000})
  response=page.goto(args.app_url+path,wait_until='networkidle')
  verified=response if response is not None else page.reload(wait_until='networkidle')
  assert verified.status==200,(name,verified.status)
  page.screenshot(path=str(ui/f'{name}.png'))
  metadata['actions'].append({'scene':name,'url':path,'http':verified.status,'capture':'Actual visible viewport'})
  page.set_viewport_size({'width':390,'height':844})
  if name=='project':
   page.goto(args.app_url+'/examples/harbourlink/cycle/2#S01',wait_until='networkidle');page.locator('#S01 .big').screenshot(path=str(details/f'{name}.png'))
  elif name=='wbs':
   page.goto(args.app_url+'/examples/harbourlink/cycle/2#S02',wait_until='networkidle');page.locator('#S02 .branch').filter(has_text='1.5 Testing and Commissioning').screenshot(path=str(details/f'{name}.png'))
  elif name=='evidence':
   page.goto(args.app_url+'/examples/harbourlink/cycle/2#S05',wait_until='networkidle')
   finding=page.locator('#S05 .finding').filter(has_text='SCH-05-001');finding.locator('.stages li').first.screenshot(path=str(details/f'{name}.png'))
  elif name=='interpretation':page.locator('#S05 .finding').filter(has_text='CST-03-004').locator('.stages li').nth(2).screenshot(path=str(details/f'{name}.png'))
  elif name=='report':page.locator('#S01 .finding').first.screenshot(path=str(details/f'{name}.png'))
  elif name=='charts':
   page.goto(args.app_url+'/examples/harbourlink/cycle/2#S04',wait_until='networkidle');page.locator('#S04 .movement-detail').screenshot(path=str(details/f'{name}.png'))
  elif name=='cycle2':page.locator('#S04 > p').first.screenshot(path=str(details/f'{name}.png'))
  elif name=='approval':page.locator('#S06 dl').screenshot(path=str(details/f'{name}.png'))
  elif name=='guide':page.locator('[data-approved-synthetic-demo]').screenshot(path=str(details/f'{name}.png'))
 page.goto(args.site_url,wait_until='networkidle');page.locator('.integration-visual').screenshot(path=str(ui/'integration.png'))
 b.close()

spec=importlib.util.spec_from_file_location('preserved_cut',HERE/'generate_harbourlink_demo.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
fonts=HERE/'fonts'
for name in ['Archivo-400.ttf','Archivo-700.ttf','OFL-Archivo.txt']:
 assert (fonts/name).is_file(), f'Missing retained licensed font: {name}'
m.FONT=str(fonts/'Archivo-400.ttf');m.BOLD=str(fonts/'Archivo-700.ttf');m.WORK=r
m.BG=(18,26,46);m.WHITE=(245,245,243);m.GOLD=(201,143,82)
captions=[
 'Schedule, cost and package meet through the Owner WBS. Source meanings remain separate.',
 '4 of 6 Owner-WBS branches have both views. Coverage is not project health.',
 'WBS 1.5 has schedule relationships. Cost coverage is absent. A professional reviews the gap.',
 'SCH-05-001 states WBS Code 1.5.1. The original source assertion remains visible.',
 'Separate example: CST-03-004. Maya’s recorded decision preserves uncertainty. Software interpretation does not approve a professional decision.',
 'One integrated report, print, phone and browser. Same findings, exact Actions and withholding.',
 'Four workbook charts retain their populations. A separately labelled detail scale shows small movements.',
 '1,613 carried forward; 1 revalidated. Together 1,614 of 1,625 remained valid, retired included.',
 'MappingVersion 2 records Maya Chen’s approval. No automatic approval is demonstrated or implied.',
 'Explore approved synthetic HarbourLink. Follow a finding to evidence, then compare both cycles.']
titles=['Different views. One Owner WBS.','4 of 6 branches. Two gaps.','WBS 1.5: cost coverage absent.','Read the original source.','Separate example. A person decides.','One report. Same governed facts.','Four charts. Clear populations.','Carry forward and revalidation.','Approval remains traceable.','Explore HarbourLink.']
for i,(old,title,caption) in enumerate(zip(m.SCENES,titles,captions)):
 m.SCENES[i]=(title,old[1],old[2],caption,old[4])
original=m.image_for
# Only the original integration diagram remains composited; all downstream UI
# comes from current captures. Complete element close-ups disclose their context.
def image_for(name,progress):
 if name=='integration':return original(name,progress)
 return Image.open(details/f'{name}.png').convert('RGB')
m.image_for=image_for
# Replace the decorative header icon with the guideline's labelled stage mark.
def stage(draw,kind,x,y):draw.rectangle((x,y+9,x+10,y+19),fill=m.GOLD)
m.icon=stage
# Archivo for text, established product arrow glyph fallback only.
old_font=m.font
def font(size,bold=False):return ImageFont.truetype(m.BOLD if bold else m.FONT,72 if size==55 else size)
m.font=font
original_render=m.render
def render(index,t):
 if index:
  # Editorial context beside one complete real mobile-layout component. No
  # unreadable full-UI interlude, cropped element or invented interactive state.
  contexts=[
   ('4 / 6','Owner-WBS branches\nschedule + cost present','Coverage, not project health.'),
   ('WBS 1.5','Testing and Commissioning\nSchedule present.\nCost coverage absent.','No zero-cost conclusion.'),
   ('SCH-05-001','Original source assertion\nWBS Code = 1.5.1','This is the present schedule view.\nThe absent cost view is bounded\nby the branch population.'),
   ('CST-03-004','Separate unresolved example\nRecorded group decision.\nUncertainty retained.','Interpretation is not approval.'),
   ('One report','Print · phone · browser\nSame exact Actions.\nSame approved findings.','Cost / forecast total withheld.'),
   ('Figure 03D · Detail','Carried forward excluded.\n1 revalidated\n4 changed · 4 new · 3 retired','Separate zero-based scale.\nWhole population: 1,625,\nincluding retired.'),
   ('1,614 / 1,625','Remained valid\n1,613 carried forward\n+ 1 re-keyed/revalidated','Denominator includes retired.'),
   ('MappingVersion 2','Maya Chen\nOwner Project Controls','Recorded whole-version approval.\nSeparate from individual decisions.'),
   ('HarbourLink','Approved synthetic example\nRead the finding.\nFollow its evidence.\nCompare approved cycles.','No uploaded data is approved.')]
  im=Image.new('RGB',(1920,1080),m.BG);draw=ImageDraw.Draw(im)
  draw.text((280,33),'HARBOURLINK / CONTROLLED SYNTHETIC REVIEW',font=font(22),fill=m.GOLD)
  draw.text((1740,32),f'{index+1:02d} / 10',font=font(24),fill=m.GOLD)
  draw.text((74,92),titles[index],font=font(66,True),fill=m.WHITE)
  draw.rectangle((72,200,1848,936),fill='white')
  label,body,boundary=contexts[index-1]
  draw.text((110,255),label,font=font(52 if len(label)>14 else 64,True),fill='#121a2e')
  draw.multiline_text((110,365),body,font=font(32),fill='#121a2e',spacing=16)
  draw.multiline_text((110,680),boundary,font=font(25),fill='#565b64',spacing=12)
  shot=image_for(m.SCENES[index][1],t/8)
  scale=min(1160/shot.width,650/shot.height)
  shot=shot.resize((round(shot.width*scale),round(shot.height*scale)),Image.Resampling.LANCZOS)
  im.paste(shot,(660+(1160-shot.width)//2,242+(650-shot.height)//2))
  draw=ImageDraw.Draw(im)
  draw.text((80,972),'Actual report / app element · source, decision and approval remain separate',font=font(25),fill=m.WHITE)
  draw.text((80,1020),'Recorded approved snapshot · fictional data only · no approval transaction demonstrated',font=font(23),fill=m.GOLD)
  draw.rectangle((0,1075,int(1920*(index+t/8)/10),1080),fill=m.GOLD)
 else:
  im=original_render(index,t)
 if min(1,t/.32,(8-t)/.32)>=1:
  draw=ImageDraw.Draw(im);draw.rectangle((66,20,238,65),fill=m.BG)
  x=72
  for word,face in [('WBS',font(25,True)),('↔',ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',25)),('LINK',font(25,True))]:
   draw.text((x,28),word,font=face,fill=m.WHITE);x+=draw.textlength(word,font=face)
 if index:
  fade=min(1,t/.32,(8-t)/.32)
  if fade<1:im=Image.blend(Image.new('RGB',(1920,1080),m.BG),im,max(0,fade))
 return im
m.render=render
if args.preview_only:
 for i in range(1,10):m.render(i,3.5).save(r/f'preview-{i+1:02d}.jpg')
 (r/'PREVIEW_PROVENANCE.json').write_text(json.dumps(metadata,indent=2))
 print('Affected scene previews retained; no film encoded in preview mode.')
 raise SystemExit(0)
segments=[]
selected={int(x) for x in args.only_scenes.split(',') if x}
for i in range(10):
 out=r/f'scene-{i+1:02d}.mp4'
 if selected and i+1 not in selected:
  if i==0 and not out.exists():shutil.copyfile(HERE/'client-closure-scene01.mp4',out)
  assert out.is_file();segments.append(out);continue
 proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','24','-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','2','-pix_fmt','yuv420p',str(out)],stdin=subprocess.PIPE)
 for n in range(192):proc.stdin.write(m.render(i,n/24).tobytes())
 proc.stdin.close();assert proc.wait()==0;segments.append(out);m.render(i,3.5).save(r/f'scene-{i+1:02d}.jpg');print('Encoded current scene',i+1,flush=True)
concat=r/'segments.txt';concat.write_text(''.join("file '"+str(f)+"'\n" for f in segments));silent=r/'picture.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy',str(silent)],check=True)
final=HERE.parent/'wbslink-video-2-how-it-works.mp4'
audio=args.audio_track or args.work.parent/'audio/video2-mix.wav'
audio_options=['-c:a','copy'] if args.audio_track else ['-c:a','aac','-b:a','192k','-ar','48000']
subprocess.run(['ffmpeg','-v','error','-y','-i',str(silent),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:v','copy']+audio_options+['-t','80','-movflags','+faststart',str(final)],check=True)
def stamp(n):return f'00:{n//60:02d}:{n%60:02d}.000'
vtt='WEBVTT\n\n'+''.join(f'{i+1}\n{stamp(i*8)} --> {stamp((i+1)*8)}\n'+('[Light rhythmic recorded instrumental]\n' if i==0 else '')+caption+'\n\n' for i,caption in enumerate(captions))
(HERE.parent/'wbslink-video-2-harbourlink.vtt').write_text(vtt.rstrip()+'\n')
metadata['music']='Advertime rhythmic direction retained; additional2dB whole-mix guitar-range attenuation at1.2/3.2kHz. -20.5LUFS target. No isolated stems or human-listening PASS claimed.'
metadata['composition']='Complete real 390px elements with editorial context; no small full-UI interlude. Original integration scene reused.'
metadata['audio_transfer']='Existing accepted AAC track copied without remix or re-encoding' if args.audio_track else 'Existing accepted WAV encoded to AAC'
metadata['changed_scenes_this_pass']=sorted(selected) if selected else list(range(1,11));metadata['separate_decision_example']='CST-03-004 is a separate unresolved example, not a claim that SCH-05-001 was individually decided.';metadata['captions']=captions;metadata['native_listening_acceptance']='Not established by technical decode, levels or screenshots.'
(r/'PROVENANCE.json').write_text(json.dumps(metadata,indent=2));print('Complete 80-second encoded cut and matching captions built.')
