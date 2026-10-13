"""Original designed Foley/ambient and restrained score; NOT sound captured from footage.

No external recording, sample pack, music, voice or new dependency is used.
Video1 uses construction/industrial/office motifs timed to the existing4s cuts.
Video2 uses sparse60BPM felt-piano/pad phrasing on the existing8s evidence scenes.
Build WAV stems with existing numpy, then two-pass EBU loudness normalization.
"""
from pathlib import Path
import argparse,json,subprocess,wave
import numpy as np
RATE=48000

def shaped_noise(rng,n,low,high,resonances=()):
 noise=rng.normal(size=n);f=np.fft.rfftfreq(n,1/RATE);s=np.fft.rfft(noise)
 shape=(1-np.exp(-(f/max(low,1))**4))*np.exp(-(f/high)**4)
 for centre,width,gain in resonances:shape+=gain*np.exp(-.5*((f-centre)/width)**2)
 a=np.fft.irfft(s*shape,n=n);return a/max(np.sqrt(np.mean(a*a)),1e-9)

def stereo(a,pan=0):return np.stack([a*np.sqrt((1-pan)/2),a*np.sqrt((1+pan)/2)],axis=1)

def pulse(t,at,width):return np.exp(-.5*((t-at)/width)**2)

def foley(duration):
 rng=np.random.default_rng(7301);n=int(duration*RATE);mix=np.zeros((n,2));t=np.arange(n)/RATE
 bed=shaped_noise(rng,n,180,1700);mix+=stereo(bed*.005)
 motifs=['crane','industrial','fans','site','office','industrial','crane','site','office','fans','crane','site','industrial','office','crane'];trace=[]
 for scene,kind in enumerate(motifs):
  start=scene*4;count=min(4*RATE,n-int(start*RATE));tt=np.arange(count)/RATE
  ramp=np.minimum(1,tt/.2)*np.minimum(1,(4-tt)/.3);gain=1
  if kind=='crane':
   # Torque ramp/hydraulic whirr: audible harmonics, not a sub-bass drone.
   rpm=58+11*np.sin(tt*.75)+18*pulse(tt,1.8,.7);phase=2*np.pi*np.cumsum(rpm)/RATE
   a=sum((.017/k)*np.sin(k*phase) for k in [2,3,5,7,9])
   a+=shaped_noise(rng,count,220,2300,[(430,90,.5),(1050,170,.3)])*.022*(.65+.35*pulse(tt,2,.9))
   a+=shaped_noise(rng,count,700,4300)*.008*(pulse(tt,.9,.2)+pulse(tt,3.1,.25))
  elif kind=='industrial':
   a=shaped_noise(rng,count,220,2100,[(420,120,.4)])*.025
   a+=np.sin(2*np.pi*180*tt)*.008*(1+.18*np.sin(2*np.pi*.65*tt))
  elif kind=='fans':
   a=shaped_noise(rng,count,420,3600,[(840,180,.4)])*.023
   a+=.006*np.sin(2*np.pi*240*tt)*(1+.12*np.sin(2*np.pi*9*tt))
  elif kind=='site':
   a=shaped_noise(rng,count,250,2800)*.022
   a+=.007*np.sin(2*np.pi*360*tt)+.003*np.sin(2*np.pi*720*tt)
  else:
   # Quiet office air and paper movement visible in the existing cut; no invented speech.
   a=shaped_noise(rng,count,300,2000)*.009
   paper=shaped_noise(rng,count,650,5200)
   a+=paper*.024*(pulse(tt,1.25,.16)+pulse(tt,2.7,.23))
  pan=[-.18,.12,0,-.08,.1][scene%5];mix[int(start*RATE):int(start*RATE)+count]+=stereo(a*ramp,pan)
  trace.append({'scene':scene+1,'start':start,'end':start+4,'motif':kind,'provenance':'original procedural designed sound; not a recording of the shown equipment'})
 return mix,trace

def score(duration):
 n=int(duration*RATE);mix=np.zeros((n,2));rng=np.random.default_rng(7302)
 chords=[[50,57,62,66],[47,54,59,62],[43,50,55,59],[45,52,57,61]]
 def note(start,length,midi,gain,pan=0,pad=False):
  start=max(0,start)
  count=min(int(length*RATE),n-int(start*RATE))
  if count<=0:return
  tt=np.arange(count)/RATE;f=440*2**((midi-69)/12)
  if pad:
   envelope=np.minimum(1,tt/.8)*np.minimum(1,np.maximum(0,(length-tt)/1.2))
   a=(np.sin(2*np.pi*f*tt)+.15*np.sin(2*np.pi*f*2*tt))*envelope*gain
  else:
   envelope=(1-np.exp(-tt/.012))*np.exp(-tt/1.7)*np.minimum(1,np.maximum(0,(length-tt)/.25))
   a=(np.sin(2*np.pi*f*tt)+.22*np.sin(2*np.pi*f*2.004*tt)+.055*np.sin(2*np.pi*f*3.01*tt))*envelope*gain
  mix[int(start*RATE):int(start*RATE)+count]+=stereo(a,pan)
 for scene in range(10):
  chord=chords[scene%4];start=scene*8
  for j,midi in enumerate(chord):note(start,8,midi,.012,pan=(j-1.5)*.18,pad=True)
  # Sparse, warm phrases; no drums, alarm tones or persistent fast arpeggio.
  for beat,step in [(0,1),(2,2),(4,3),(6,2)]:note(start+beat+.018*float(rng.uniform(-1,1)),2.5,chord[step]+12,.033,pan=.2 if step%2 else -.2)
  note(start,4,chord[0],.023)
 return mix,[{'scene':i+1,'start':i*8,'end':(i+1)*8,'motif':'sparse60BPM piano and warm pad; original procedural instrumental'} for i in range(10)]

def write_wav(path,mix):
 ramp=np.minimum(1,np.arange(len(mix))/RATE/.6)*np.minimum(1,(len(mix)-np.arange(len(mix)))/RATE/.9);mix*=ramp[:,None]
 assert np.max(np.abs(mix))<1,'Stem clips before normalization'
 with wave.open(str(path),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(RATE);f.writeframes((mix*32767).astype('<i2').tobytes())

def normalize(src,dst,target):
 base=['ffmpeg','-y','-hide_banner','-i',str(src)]
 first=subprocess.run(base+['-af',f'loudnorm=I={target}:TP=-2:LRA=7:print_format=json','-f','null','-'],capture_output=True,text=True,check=True).stderr
 measured=json.loads(first[first.rfind('{'):first.rfind('}')+1])
 filt=f"loudnorm=I={target}:TP=-2:LRA=7:measured_I={measured['input_i']}:measured_TP={measured['input_tp']}:measured_LRA={measured['input_lra']}:measured_thresh={measured['input_thresh']}:offset={measured['target_offset']}:linear=true:print_format=json"
 second=subprocess.run(base+['-af',filt,'-ar',str(RATE),'-c:a','pcm_s24le',str(dst)],capture_output=True,text=True,check=True).stderr
 summary=json.loads(second[second.rfind('{'):second.rfind('}')+1]);return {'target_lufs':target,'true_peak_limit_db':-2,'first_pass':measured,'final_wav':summary}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);args=p.parse_args();args.work.mkdir(parents=True,exist_ok=True);record=[]
 for number,duration,fn,target in [(1,60.01,foley,-18),(2,80,score,-19)]:
  mix,trace=fn(duration);raw=args.work/f'video{number}-stem.wav';final=args.work/f'video{number}-mix.wav';write_wav(raw,mix);report=normalize(raw,final,target);record.append({'video':number,'seconds':duration,'scenes':trace,'loudness':report,'listening':'Human/device listening pending; engineering metrics are not subjective acceptance.'})
 (args.work/'mix-provenance.json').write_text(json.dumps({'no_third_party_assets':True,'not_captured_location_sound':True,'mixes':record},indent=2));print('Original Foley/score WAV mixes and two-pass loudness evidence built.')
