from pathlib import Path
import json, os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(os.environ.get('WBSLINK_SHOW_OUTPUT', ROOT / 'evidence' / 'commercial-experience'))
OUT.mkdir(parents=True, exist_ok=True)
URL = 'http://127.0.0.1:8000/'
results = {'url': URL, 'views': {}}
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=os.environ.get('WBSLINK_BROWSER_EXECUTABLE'))
    try:
        for name, width, height in [('desktop', 1440, 1000), ('mobile', 390, 844)]:
            page = browser.new_page(viewport={'width': width, 'height': height})
            print(f'{name}: loading website', flush=True)
            page.goto(URL, wait_until='networkidle')
            page.screenshot(path=str(OUT / f'website-{name}.png'), full_page=True)
            metrics = page.evaluate('''() => ({
                scrollWidth: document.documentElement.scrollWidth,
                clientWidth: document.documentElement.clientWidth,
                scrollHeight: document.documentElement.scrollHeight,
                title: document.title,
                h1: document.querySelector('h1')?.innerText || '',
                videos: document.querySelectorAll('video').length,
                brokenImages: [...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.src)
            })''')
            metrics['horizontalOverflow'] = metrics['scrollWidth'] > metrics['clientWidth'] + 1
            assert not metrics['horizontalOverflow'], metrics
            assert not metrics['brokenImages'], metrics
            assert metrics['videos'] >= 2, metrics
            metrics['media'] = []
            for index in range(2):
                video = page.locator('video').nth(index)
                print(f'{name}: checking video {index + 1}', flush=True)
                video.scroll_into_view_if_needed()
                video.evaluate('(v) => { v.preload = "auto"; v.load(); }')
                page.wait_for_function('(i) => document.querySelectorAll("video")[i].readyState >= 2', arg=index)
                state = video.evaluate('''(v) => ({duration: v.duration, width: v.videoWidth,
                    height: v.videoHeight, controls: v.controls, playsInline: v.playsInline,
                    error: v.error?.code || null, poster: v.poster})''')
                assert state['controls'] and state['playsInline'] and not state['error'], state
                assert state['width'] > 0 and state['height'] > 0, state
                if index == 0:
                    assert abs(state['duration'] - 60) < .05, state
                    page.wait_for_function('''() => {
                        const v = document.querySelector('video');
                        return v.textTracks.length === 1 && v.textTracks[0].cues?.length === 15;
                    }''')
                    state['captions'] = video.evaluate('(v) => ({mode: v.textTracks[0].mode, cues: v.textTracks[0].cues.length})')
                    assert state['captions']['mode'] == 'showing', state
                else:
                    assert 65 <= state['duration'] <= 105, state
                video.evaluate('(v) => { v.play().catch(e => { v.dataset.playError = e.name; }); }')
                page.wait_for_function('(i) => document.querySelectorAll("video")[i].currentTime > .5', arg=index)
                state['playbackAdvanced'] = True
                video.evaluate('(v) => v.pause()')
                for seconds in ([4.5, 32.5, 56.5] if index == 0 else [10.5]):
                    video.evaluate('(v, t) => { v.currentTime = t; }', seconds)
                    page.wait_for_function('''({i,t}) => {
                        const v = document.querySelectorAll('video')[i];
                        return !v.seeking && v.readyState >= 2 && Math.abs(v.currentTime - t) < .1;
                    }''', arg={'i': index, 't': seconds})
                    video.screenshot(path=str(OUT / f'video{index+1}-{name}-{int(seconds)}s.png'))
                metrics['media'].append(state)
            for target in ('how-to.html', 'leaderboard.html', 'healthcheck.html',
                           'downloads/harbourlink-practice-project.zip'):
                response = page.request.get(URL + target)
                assert response.ok, (target, response.status)
            metrics['localJourneyLinks'] = 'PASS'
            results['views'][name] = metrics
            page.close()
    finally:
        browser.close()
(OUT / 'browser-check.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
print(json.dumps(results, indent=2))
