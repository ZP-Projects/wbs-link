from pathlib import Path
import importlib.util,subprocess,json
from PIL import Image
import numpy as np
from playwright.sync_api import sync_playwright
import argparse
p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--site-url',default='http://127.0.0.1:8813/');p.add_argument('--base-video',type=Path,required=True);args=p.parse_args()
R=args.work;S=Path(__file__).resolve().parent;W=R/'video-patches';W.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True);page=b.new_page(viewport={'width':1440,'height':1000});page.goto(args.site_url,wait_until='networkidle');page.locator('.integration-visual img').screenshot(path=str(S/'harbourlink_ui/integration.png'));b.close()
recording=R/'recordings/cycle2.webm';probe=W/'probe';probe.mkdir(exist_ok=True)
subprocess.run(['ffmpeg','-y','-v','error','-i',str(recording),'-vf','fps=24','-q:v','3',str(probe/'%04d.jpg')],check=True)
frames=list(sorted(probe.glob('*.jpg')));real=[]
for f in frames:
 a=np.array(Image.open(f).resize((160,100)));fraction=float(np.mean(np.min(a,axis=2)<230))
 if fraction>.01:real.append(f)
assert real;motion=W/'motion/cycle2';motion.mkdir(parents=True,exist_ok=True)
import shutil
for i in range(192):shutil.copyfile(real[min(i,len(real)-1)],motion/f'{i+1:04d}.jpg')
(S/'harbourlink_ui/recordings').mkdir(exist_ok=True);shutil.copyfile(recording,S/'harbourlink_ui/recordings/cycle2.webm')
shutil.copyfile(real[0],S/'harbourlink_ui/cycle2.png')
metadata={'changed_visual_scenes':[1,8],'retained_visual_scenes':[2,3,4,5,6,7,9,10],'original_duration_seconds':80,'timeline_preserved':True,'scene8_source':'actual final-label local browser recording; full viewport, no fake decision','raw_frames':len(frames),'real_frames':len(real),'loading_frames_removed':len(frames)-len(real),'frame_order_preserved':True}
(W/'patch-provenance.json').write_text(json.dumps(metadata,indent=2))
spec=importlib.util.spec_from_file_location('cut',S/'generate_harbourlink_demo.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.WORK=W
for idx in [0,7]:
 out=W/f'scene{idx+1}.mp4';cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','24','-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','2','-pix_fmt','yuv420p',str(out)];proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for n in range(192):proc.stdin.write(m.render(idx,n/24).tobytes())
 proc.stdin.close();assert proc.wait()==0;m.render(idx,3.2).save(W/f'scene{idx+1}-actual.jpg')
 if idx==0:m.render(idx,3.2).save(S.parent/'wbslink-video-2-how-it-works.jpg')
 print('Patched actual scene',idx+1,flush=True)
base=args.base_video;final=W/'video2-final.mp4'
subprocess.run(['ffmpeg','-y','-v','error','-i',str(base),'-i',str(W/'scene1.mp4'),'-i',str(W/'scene8.mp4'),'-i',str(R/'audio/video2-mix.wav'),'-filter_complex',"[1:v]setpts=PTS-STARTPTS[first];[2:v]setpts=PTS-STARTPTS+56/TB[cycle];[0:v][first]overlay=0:0:enable='between(t,0,7.9999)'[one];[one][cycle]overlay=0:0:enable='between(t,56,63.9999)'[v]",'-map','[v]','-map','3:a:0','-t','80','-c:v','libx264','-preset','veryfast','-crf','18','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(final)],check=True)
shutil.copyfile(final,S.parent/'wbslink-video-2-how-it-works.mp4');print('Full80s existing film preserved;2affected scenes patched and new original score mixed.')
