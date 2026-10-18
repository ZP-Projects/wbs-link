"""Customer story cut, using approved public-safe report fields and retained audio.

Purpose-designed explanatory exhibits, not a fabricated application transaction.
Film 1 is never opened for writing. No new voice, music or media dependency.
"""
from pathlib import Path
import argparse,json,subprocess,hashlib,textwrap
from PIL import Image,ImageDraw,ImageFont

HERE=Path(__file__).resolve().parent;VIDEO=HERE.parent
NAVY='#121A2E';PAPER='#F5F5F3';GREY='#565B64';COGNAC='#8F5A28'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build(model_path,work):
 m=json.loads(Path(model_path).read_text());work=Path(work).resolve();work.mkdir(parents=True,exist_ok=True)
 film1=VIDEO/'wbslink-video-1-challenge.mp4';before=digest(film1)
 original=VIDEO/'wbslink-video-2-how-it-works.mp4';audio=work/'retained-film2-audio.aac'
 if not audio.exists():subprocess.run(['ffmpeg','-v','error','-y','-i',str(original),'-vn','-c:a','copy','-f','adts',str(audio)],check=True)
 action=next(f['next'] for f in m['findings'] if (f.get('branch') or {}).get('code')=='1.5')
 prev=m['previous_report_summary'];unresolved=sum(n for k,n in m['outcomes']['rows'] if 'UNSURE' in k)
 captions=[
  'HarbourLink compares schedule, cost and work packages through the owner’s Work Breakdown Structure.',
  'Testing and Commissioning has schedule relationships, but no cost relationships in the approved source set.',
  action,
  'Check the original source: its WBS Code is 1.5.1. An assertion is not an individual professional confirmation.',
  'Review the interpretation and contrary evidence. The work-area count establishes the absent cost view; one example alone does not.',
  'Software interpretation does not approve a professional decision. Keep uncertainty where evidence does not settle the relationship.',
  'No automatic approval is demonstrated or implied. Maya Chen’s recorded whole-version approval does not individually confirm every relationship.',
  f'July keeps both gaps. Unresolved relationships increase from {prev["UNSURE"]} to {unresolved}, including one package relationship.',
  'July has 1,622 current relationships plus three retired versions: 1,625 relationship versions in all.',
  'Read the exact Action and recorded changes. Follow the source and decision evidence before drawing a project conclusion.'
 ]
 scenes=[
  ('Bring the views to the same scope.','Owner Work Breakdown Structure','Schedule\nCost / forecast\nWork packages','Each source relates independently through the owner’s hierarchy of project work.'),
  ('The gap is a management question.','Testing and Commissioning','Schedule: 180 relationships\nCost relationships: ABSENT','This does not establish zero cost, missing work or an overrun.'),
  ('Check whether the gap is expected.','Exact recorded Action',action,'The Action is preserved verbatim. No assignee, deadline or project impact is invented.'),
  ('Read what the original source asserts.','Original source assertion','WBS Code = 1.5.1','An original assertion is evidence to inspect. It is not an individual professional confirmation.'),
  ('Separate interpretation from decision.','Review the evidence','Original assertion\nInterpretation\nContrary evidence','One source example shows a present relationship. The full work-area count establishes the absent cost view.'),
  ('Leave unsupported conclusions open.','Record the decision scope','A separate cost example keeps\na group of 81 relationships unresolved.','That bounded decision is not a decision on every unresolved relationship.'),
  ('Approve the reporting position separately.','Recorded whole-version approval','Maya Chen\nOwner Project Controls','Fictional recorded attribution, not verified professional identity. Approval does not individually confirm every relationship.'),
  ('Changed evidence needs renewed review.','June to July',f'Unresolved: {prev["UNSURE"]} to {unresolved}\nPackage unresolved: 0 to 1\nTwo coverage gaps remain.','The records do not establish the cause, cost effect or schedule effect.'),
  ('Keep current work separate from history.','July relationship populations','1,622 current\n3 retired historical versions\n1,625 versions in all','Recorded movement: 1,613 carried forward; 1 revalidated; 4 changed; 4 new; 3 retired. These are not individual source confirmations.'),
  ('Follow one finding all the way through.','Read the HarbourLink report','Exact Action\nOriginal source\nProfessional decision scope\nSeparate approval','Compare June and July before drawing a project conclusion. Fictional example only.')
 ]
 fonts=HERE/'fonts'
 def font(size,bold=False):return ImageFont.truetype(str(fonts/('Archivo-700.ttf' if bold else 'Archivo-400.ttf')),size)
 def wrap(draw,text,face,width):
  lines=[]
  for para in str(text).split('\n'):
   line=''
   for word in para.split():
    attempt=(line+' '+word).strip()
    if line and draw.textlength(attempt,font=face)>width:lines.append(line);line=word
    else:line=attempt
   lines.append(line)
  return lines
 def write(draw,text,x,y,width,size,bold=False,color=NAVY,leading=1.3):
  face=font(size,bold);lines=wrap(draw,text,face,width)
  for line in lines:draw.text((x,y),line,font=face,fill=color);y+=size*leading
  return y
 outputs=[]
 for phone in [False,True]:
  W,H=(1080,1920) if phone else (1920,1080);tag='phone' if phone else 'landscape';folder=work/tag;folder.mkdir(exist_ok=True);segments=[]
  for i,(title,label,body,boundary) in enumerate(scenes):
   im=Image.new('RGB',(W,H),NAVY);d=ImageDraw.Draw(im);margin=68 if phone else 90
   d.rectangle((0,0,W,10),fill=COGNAC)
   brand_size=38 if phone else 33;bx=margin
   for part,face in [('WBS',font(brand_size,True)),('↔',ImageFont.truetype(str(VIDEO.parents[0]/'assets/fonts/DejaVuSans.ttf'),brand_size)),('LINK · HarbourLink',font(brand_size,True))]:
    d.text((bx,55),part,font=face,fill=PAPER);bx+=d.textlength(part,font=face)+3
   write(d,'FICTIONAL APPROVED RECORD · EXPLANATORY EXHIBIT',margin,115,W-margin*2,25 if phone else 24,False,PAPER)
   y=write(d,title,margin,205 if phone else 180,W-margin*2,70 if phone else 68,True,PAPER,1.15)
   top=max(y+65,510 if phone else 370);bottom=H-(225 if phone else 170)
   d.rectangle((margin,top,W-margin,bottom),fill=PAPER)
   y=write(d,label,margin+38,top+38,W-margin*2-76,42 if phone else 38,True,COGNAC)
   y=write(d,body,margin+38,y+38,W-margin*2-76,59 if phone else (48 if len(body)>100 or len(body.split('\n'))>=4 else 64),True,NAVY,1.3)
   y=write(d,boundary,margin+38,y+55,W-margin*2-76,42 if phone else 34,False,GREY,1.3)
   assert y<bottom-18,(tag,i+1,'material text overflows',y,bottom)
   write(d,f'{i+1:02d} / 10 · Source, decision and approval remain separate.',margin,H-125,W-margin*2,28 if phone else 27,False,PAPER)
   frame=folder/f'scene-{i+1:02d}.png';im.save(frame)
   out=folder/f'scene-{i+1:02d}.mp4';segments.append(out)
   subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-i',str(frame),'-t','8','-r','24','-vf','fade=t=in:st=0:d=0.25,fade=t=out:st=7.75:d=0.25','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','2','-pix_fmt','yuv420p',str(out)],check=True)
   print('ENCODED',tag,i+1,flush=True)
  listing=folder/'segments.txt';listing.write_text(''.join("file '"+str(p)+"'\n" for p in segments));silent=folder/'picture.mp4'
  subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(listing),'-c','copy',str(silent)],check=True)
  final=VIDEO/('wbslink-video-2-how-it-works-phone.mp4' if phone else 'wbslink-video-2-how-it-works.mp4')
  subprocess.run(['ffmpeg','-v','error','-y','-i',str(silent),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','copy','-t','80','-movflags','+faststart',str(final)],check=True);outputs.append({'file':final.name,'sha256':digest(final)})
 def stamp(t):return f'00:{t//60:02d}:{t%60:02d}.000'
 vtt='WEBVTT\n\n'+''.join(f'{i+1}\n{stamp(i*8)} --> {stamp((i+1)*8)}\n'+('[Recorded instrumental music]\n' if i==0 else '')+c+'\n\n' for i,c in enumerate(captions))
 for name in ['wbslink-video-2-harbourlink.vtt','wbslink-video-2-how-it-works-phone.vtt']:(VIDEO/name).write_text(vtt.rstrip()+'\n')
 assert digest(film1)==before
 (work/'PROVENANCE.json').write_text(json.dumps({'model_sha256':digest(Path(model_path)),'source':'Approved fictional report fields, no hidden truth','film1_unchanged_sha256':before,'retained_audio_sha256':digest(audio),'audio':'Retained original instrumental AAC packet stream, trimmed at 80 seconds; no new speech/voice claim','composition':'Purpose-designed explanatory exhibits, not an application transaction','outputs':outputs,'captions':captions,'native_human_listening':'NOT VERIFIED'},indent=2)+'\n')
 print('BUILT full 80s landscape/phone films; Film 1 unchanged',flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--model',required=True);ap.add_argument('--work',required=True);a=ap.parse_args();build(a.model,a.work)
