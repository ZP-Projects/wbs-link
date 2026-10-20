"""Picture-anchored restrained soundtrack from already retained CC0 recordings.

No remote media or new dependencies. Foley only in identifiable visible action
windows; hidden footfalls and mouse clicks are omitted rather than fabricated.
Frame/sample timing is technical evidence, not subjective listening acceptance.
"""
from pathlib import Path
import argparse,json,subprocess,wave,hashlib
import numpy as np
ROOT=Path(__file__).parent;RATE=48000;FPS=24

def decoded(name,seconds=None,filters=''):
 cmd=['ffmpeg','-v','error','-i',str(ROOT/'assets'/name)]
 if seconds:cmd+=['-t',str(seconds)]
 if filters:cmd+=['-af',filters]
 cmd+=['-ar',str(RATE),'-ac','2','-f','f32le','-']
 return np.frombuffer(subprocess.check_output(cmd),'<f4').reshape(-1,2).copy()

def write(path,x):
 with wave.open(str(path),'wb') as f:
  f.setnchannels(2);f.setsampwidth(2);f.setframerate(RATE);f.writeframes((np.clip(x,-.95,.95)*32767).astype('<i2').tobytes())

def main():
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args();a.work.mkdir(parents=True,exist_ok=True)
 # A legally reusable rhythmic instrumental direction from the previously
 # owner-accepted creative sample. Exact earlier Planning Planet music was not
 # recovered. Do not attribute this track to that historical contribution.
 bed=decoded('advertime.mp3',60,'highpass=f=80,bass=f=200:g=-7:t=q:w=0.7,equalizer=f=1200:t=q:w=0.65:g=-6,equalizer=f=3200:t=q:w=0.9:g=-5,loudnorm=I=-23:TP=-3:LRA=8,afade=t=in:d=1.5,afade=t=out:st=57:d=3')
 film=np.zeros((60*RATE,2),np.float32);film[:min(len(bed),len(film))]=bed[:len(film)]
 cues=[]
 def cue(name,start_frame,end_frame,gain,perspective,observation):
  x=decoded(name,filters='highpass=f=110,lowpass=f=6000');x/=max(float(np.max(abs(x))),.001)
  count=(end_frame-start_frame)*RATE//FPS
  x=np.tile(x,(int(np.ceil(count/len(x))),1))[:count]
  fade=min(int(.07*RATE),count//2);x[:fade]*=np.linspace(0,1,fade)[:,None];x[-fade:]*=np.linspace(1,0,fade)[:,None]
  start=start_frame*RATE//FPS;film[start:start+count]+=x*gain
  cues.append({'asset':name,'onset_frame':start_frame,'offset_frame_exclusive':end_frame,'onset_seconds':start_frame/FPS,'offset_seconds':end_frame/FPS,'sample_onset':start,'sample_offset':start+count,'perspective':perspective,'visible_basis':observation,'gain':gain,'recording_sha256':hashlib.sha256((ROOT/'assets'/name).read_bytes()).hexdigest()})
 for start in [8,36]:cue('machine.ogg',int((start+.25)*FPS),int((start+1.875)*FPS),.05,'Close equipment, softened mechanical bed','Industrial equipment close-up ends before the wider construction view; no percussive impact is invented.')
 for start in [16,32,52]:
  cue('keyboard.wav',int((start+.25)*FPS),int((start+1.625)*FPS),.085,'Close hand/keyboard','Actual keyboard close-up. Cue ends before document/tablet cut.')
  cue('paper.ogg',int((start+2.375)*FPS),int((start+3.375)*FPS),.055,'Near desk, restrained rustle','Paper handling in the widened office shot; no keyboard or mouse sound continues across the cut.')
 manifest={'fps':FPS,'sample_rate':RATE,'duration_seconds':60,'source_video':'../wbslink-video-1-original.mp4','source_video_sha256':hashlib.sha256((ROOT.parent/'wbslink-video-1-original.mp4').read_bytes()).hexdigest(),'music':{'track':'Advertime','creator':'Rafael Krux','licence':'CC0, retained FreePD provenance','sha256':hashlib.sha256((ROOT/'assets/advertime.mp3').read_bytes()).hexdigest(),'reference':'Previously accepted creative musical direction; exact Planning Planet soundtrack not recovered. This is not a claim of that historical track.'},'bass_control':'V1 recorded music low shelf at200Hz/-7dB removes excessive bass emphasis; retained rhythm, no procedural hum.',
        'cue_rule':'Onset/offset aligned to actual identifiable shot/action windows at24fps. Exact human-perceived gesture synchronisation remains a listening-review criterion. No footsteps over camera movement; no mouse clicks over tablets or off-screen hands.','removed_unsupported_cues':['footsteps: visible footfalls unavailable','mouse: contact/button actions not demonstrable in the wide desk footage','tablet: no physical mouse effect assigned'],'events':cues,'human_listening':'Not performed by Engineering; one uninterrupted ordinary-speaker/headphone and physical-phone session remains required.'}
 write(a.work/'video1-picture-mix.wav',film)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(a.work/'video1-picture-mix.wav'),'-af','loudnorm=I=-20:TP=-2:LRA=8,alimiter=limit=0.79:level=disabled','-ar',str(RATE),str(a.work/'video1-mix.wav')],check=True)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(ROOT/'assets/advertime.mp3'),'-t','80','-af','equalizer=f=1200:t=q:w=0.65:g=-6,equalizer=f=3200:t=q:w=0.9:g=-5,afade=t=in:d=1.5,afade=t=out:st=77:d=3,loudnorm=I=-20.5:TP=-2:LRA=8','-ar',str(RATE),'-ac','2',str(a.work/'video2-mix.wav')],check=True)
 (a.work/'cue-map.json').write_text(json.dumps(manifest,indent=2));print('Picture-anchored licensed audio built; human listening remains unobserved.')
if __name__=='__main__':main()
