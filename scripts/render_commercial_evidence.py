from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evidence' / 'commercial-experience'
OUT.mkdir(parents=True, exist_ok=True)
URL = 'http://127.0.0.1:8000/'
results = {'url': URL, 'views': {}}
with sync_playwright() as p:
    browser = p.chromium.launch()
    try:
        for name, width, height in [('desktop', 1440, 1000), ('mobile', 390, 844)]:
            page = browser.new_page(viewport={'width': width, 'height': height})
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
            results['views'][name] = metrics
            page.close()
    finally:
        browser.close()
(OUT / 'browser-check.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
print(json.dumps(results, indent=2))
