"""Mix licensed recordings against the preserved cuts; never regenerate visuals."""
from pathlib import Path
import argparse, json, subprocess, wave
import numpy as np

ROOT = Path(__file__).parent
RATE = 48000

def recording(name):
    data = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(ROOT/'assets'/name),
        '-af', 'highpass=f=100,lowpass=f=7000', '-ar', str(RATE), '-ac', '2', '-f', 'f32le', '-'])
    x = np.frombuffer(data, '<f4').reshape(-1, 2).copy()
    return x / max(float(np.max(np.abs(x))), .001)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args(); args.work.mkdir(parents=True, exist_ok=True)
    film = np.zeros((60*RATE, 2), dtype=np.float32); events = []
    def place(name, start, seconds=None, gain=.2, offset=0):
        x = recording(name)
        if not len(x):raise ValueError('Empty licensed recording: '+name)
        # Short Foley recordings may repeat; offset never discards the entire take.
        x = x[int(offset*RATE)%len(x):]
        if seconds is not None:
            count = int(seconds*RATE)
            x = np.tile(x, (int(np.ceil(count/len(x))), 1))[:count]
        fade = min(int(.06*RATE),len(x)//2)
        if fade:
            x[:fade] *= np.linspace(0,1,fade)[:,None]
            x[-fade:] *= np.linspace(1,0,fade)[:,None]
        position = int(start*RATE); end = min(len(film),position+len(x))
        film[position:end] += x[:end-position]*gain
        events.append({'recording':name,'start':start,'end':end/RATE,'gain':gain})
    # Cue windows verified against the preserved 60-second film. The warehouse
    # cuts change to tablet/plan handling after two seconds; footsteps stop there.
    for cut in [0,6,10,14]:
        place('site.ogg',cut*4,4,gain=.055,offset=(cut%3)*2)
    for cut in [2,9]:
        place('machine.ogg',cut*4,2.1,gain=.08)
        place('machine.ogg',cut*4+2.1,1.9,gain=.035,offset=2.1)
    for cut in [1,5,12]:
        for step,t in enumerate([.28,.88,1.48]):
            place(f'step-hard-{step%4}.wav',cut*4+t,gain=.18)
        place('mouseclick.wav',cut*4+2.72,gain=.085)
        place('mouserelease.wav',cut*4+2.84,gain=.055)
    # Mouse-hand workstation footage, not generic typing over every desk shot.
    for cut in [3,7,11]:
        place('mouseclick.wav',cut*4+.86,gain=.20)
        place('mouserelease.wav',cut*4+.98,gain=.13)
        place('keyboard.wav',cut*4+1.62,.60,gain=.08,offset=.5)
    # Keyboard close-up lasts approximately one second, then tablet/plan handling.
    for cut in [4,8,13]:
        place('keyboard.wav',cut*4+.08,1.02,gain=.17,offset=(cut%3)*.2)
        place('mouseclick.wav',cut*4+1.88,gain=.085)
        place('mouserelease.wav',cut*4+2.00,gain=.055)
        place('paper.ogg',cut*4+2.75,.55,gain=.07)
    cue_sheet={
        'visual_cut_seconds':4,'preserved_visuals':True,
        'footsteps':'Designed Foley inside observed walking windows only; individual footfalls are not visible.',
        'input':'Mouse/keyboard recordings used for designed input cues; tablet taps are Foley approximations, not original location sound.',
        'perspective':'Mechanical foreground reduced after close-up changes to the distant corridor; site panoramas use lower recorded ambience.',
        'listening_acceptance':'Unperformed by Engineering; codecs/levels do not establish human listening acceptance.',
        'events':events}
    (args.work/'cue-sheet.json').write_text(json.dumps(cue_sheet,indent=2))
    raw=args.work/'video1-recordings.wav'
    with wave.open(str(raw),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(RATE)
        w.writeframes((np.clip(film,-.95,.95)*32767).astype('<i2').tobytes())
    (args.work/'recording-timeline.json').write_text(json.dumps(events,indent=2))
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw),'-af',
        'loudnorm=I=-18:TP=-2:LRA=8,alimiter=limit=0.63:level=disabled','-ar',str(RATE),str(args.work/'video1-mix.wav')],check=True)
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(ROOT/'assets/advertime.mp3'),'-t','80',
        '-af','equalizer=f=1200:t=q:w=0.65:g=-4,equalizer=f=3200:t=q:w=0.9:g=-3,afade=t=in:d=1.5,afade=t=out:st=77:d=3,loudnorm=I=-20.5:TP=-2:LRA=8',
        '-ar',str(RATE),'-ac','2',str(args.work/'video2-mix.wav')],check=True)
    print('Recorded-effects mix and recorded instrumental candidate built; human listening pending.')

if __name__ == '__main__':main()
