"""Actual current UI close-ups for normal phone playback, with matching timeline.

Complete captured elements, no fictitious clicks or approval transaction. Retains
all ten scenes and copies the exact final desktop AAC stream. Captions are separate.
"""
from pathlib import Path
import argparse,subprocess,json,shutil
from PIL import Image,ImageDraw,ImageFont
from playwright.sync_api import sync_playwright
HERE=Path(__file__).parent;p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--app-url',required=True);p.add_argument('--site-url',required=True);p.add_argument('--only-scenes',default='');args=p.parse_args();R=args.work;R.mkdir(parents=True,exist_ok=True)
titles=['One Owner WBS','4 of 6 branches','Cost coverage absent','Read the source','Separate example','Exact professional Action','Small cycle movements','1,614 remain valid','Separate approval','Explore HarbourLink']
shots=[];meta={'format':'1080x1920 portrait, actual390px UI elements at3x device density','timeline':'Same10 scenes ×8 seconds as80-second desktop film','approval_transaction':False,'captions':'Separate optional VTT, disabled by default'}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium');pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=3)
 pg.goto(args.site_url,wait_until='networkidle');pg.locator('.owner-map').screenshot(path=str(R/'01.png'));shots.append(R/'01.png')
 for i,(url,selector,filtertext,nth) in enumerate([
  ('/examples/harbourlink/cycle/2#S01','#S01 .big',None,0),
  ('/examples/harbourlink/cycle/2#S01','#S01 .coverage-matrix',None,0),
  ('/examples/harbourlink/cycle/2#S05','#S05 .finding','SCH-05-001',0),
  ('/examples/harbourlink/cycle/2#S05','#S05 .finding','CST-03-004',2),
  ('/examples/harbourlink/cycle/2#S01','#S01 .finding',None,0),
  ('/examples/harbourlink/cycle/2#S04','#S04 .movement-detail',None,0),
  ('/examples/harbourlink/cycle/2#S04','#S04 > p',None,0),
  ('/examples/harbourlink/cycle/2#S06','#S06 dl',None,0),
  ('/projects/harbourlink','[data-approved-synthetic-demo]',None,0)],2):
  pg.goto(args.app_url+url,wait_until='networkidle');el=pg.locator(selector)
  if filtertext:el=el.filter(has_text=filtertext)
  el=el.first
  if i in [4,5]:el=el.locator('.stages li').nth(nth)
  if i==6:el=el.locator('p').last
  if i==10:el=el.locator('a.btn.primary').first
  # Capture the complete owning element, not a cropped viewport fragment.
  target=R/f'{i:02}.png';el.screenshot(path=str(target));shots.append(target)
 b.close()
fonts=HERE/'fonts'
def face(size,bold=False):return ImageFont.truetype(str(fonts/('Archivo-700.ttf' if bold else 'Archivo-400.ttf')),size)
selected={int(x) for x in args.only_scenes.split(',') if x}
segments=[]
for i,shot in enumerate(shots):
 if selected and i+1 not in selected:
  old=R/f'scene-{i+1:02}.mp4';assert old.is_file();segments.append(old);continue
 im=Image.new('RGB',(1080,1920),'#121A2E');d=ImageDraw.Draw(im)
 d.text((66,68),'WBS LINK · HARBOURLINK',font=face(38,True),fill='#F5F5F3')
 d.text((66,150),f'{i+1:02} / 10',font=face(36),fill='#C98F52')
 import textwrap
 lines=textwrap.wrap(titles[i],width=24)
 d.multiline_text((66,224),'\n'.join(lines),font=face(66,True),fill='#F5F5F3',spacing=10)
 subtitles=['Your common list of project work','Owner-WBS coverage, not health','WBS 1.5 Testing and Commissioning','SCH-05-001 · source assertion','CST-03-004 · unresolved group','Exact wording from approved report','Separate scale, carried excluded','1,613 carried +1 revalidated','Recorded MappingVersion 2','Read-only synthetic demonstration']
 d.text((66,340),subtitles[i],font=face(35),fill='#C98F52')
 picture=Image.open(shot).convert('RGB');scale=min(948/picture.width,1220/picture.height)
 picture=picture.resize((round(picture.width*scale),round(picture.height*scale)),Image.Resampling.LANCZOS)
 y=420+(1220-picture.height)//2
 # Integration is the actual navy website composition; other captures are complete white UI elements.
 if i:d.rectangle((48,400,1032,1660),fill='white')
 im.paste(picture,((1080-picture.width)//2,y))
 d=ImageDraw.Draw(im)
 if i==9:d.multiline_text((90,610),'Choose a finding.\nFollow its own evidence.\nCompare the approved cycles.',font=face(47,True),fill='#121A2E',spacing=25)
 if i==1:d.multiline_text((90,1320),'Owner-WBS branches\nSchedule + cost present\nCoverage is not project health.',font=face(44),fill='#121A2E',spacing=18)
 d.text((66,1740),'Fictional approved snapshot',font=face(39),fill='#F5F5F3');d.text((66,1804),'Professional authority stays separate',font=face(32),fill='#C98F52')
 f=R/f'frame-{i+1:02}.png';im.save(f);out=R/f'scene-{i+1:02}.mp4'
 subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-i',str(f),'-t','8','-vf','fps=24,format=yuv420p','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','2',str(out)],check=True);segments.append(out);print('Encoded portrait scene',i+1,flush=True)
concat=R/'segments.txt';concat.write_text(''.join("file '"+str(f)+"'\n" for f in segments));silent=R/'picture.mp4';subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy',str(silent)],check=True)
final=HERE.parent/'wbslink-video-2-how-it-works-phone.mp4';subprocess.run(['ffmpeg','-v','error','-y','-i',str(silent),'-i',str(HERE.parent/'wbslink-video-2-how-it-works.mp4'),'-map','0:v:0','-map','1:a:0','-c','copy','-t','80','-movflags','+faststart',str(final)],check=True)
shutil.copyfile(HERE.parent/'wbslink-video-2-harbourlink.vtt',HERE.parent/'wbslink-video-2-how-it-works-phone.vtt');meta['source_captures']=[str(x.name) for x in shots];(R/'PROVENANCE.json').write_text(json.dumps(meta,indent=2));print('Full80-second phone film and matching optional captions built.')
