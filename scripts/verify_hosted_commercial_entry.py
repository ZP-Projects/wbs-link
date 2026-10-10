"""Verify the actual hosted public-preview-to-private-preview entry on two viewports.
No login secrets, project data, or private application writes are used.
"""
from __future__ import annotations
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

SITE = "https://issue-35-execution-gate-v2-production.up.railway.app/"
APP = "https://issue-35-execution-gate-production.up.railway.app/"
OUT = Path("evidence/commercial-experience/hosted-entry.json")
OUT.parent.mkdir(parents=True, exist_ok=True)
results = {"commercialPreview": SITE, "privateAppPreview": APP, "views": {}}
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    try:
        for label, width, height in (("desktop",1440,1000),("mobile",390,844)):
            context = browser.new_context(viewport={"width": width,"height":height})
            page = context.new_page()
            response = page.goto(SITE,wait_until="domcontentloaded",timeout=30000)
            assert response is not None and response.status == 200, (label,"site",response and response.status)
            assert page.locator("video").count() == 2, label
            assert page.locator("#practice a[href$='harbourlink-practice-project.zip']").count() == 1
            link = page.locator("#app a.btn.primary")
            assert link.count() == 1, label
            assert link.get_attribute("href") == APP
            assert link.get_attribute("target") == "_blank"
            with page.expect_popup(timeout=30000) as opening:
                link.click()
            app = opening.value
            app.wait_for_load_state("domcontentloaded",timeout=30000)
            assert app.url.startswith(APP), (label,app.url)
            visible = app.locator("body").inner_text(timeout=20000)
            assert visible.strip() and ("WBS" in visible or "project" in visible.lower()), (label,visible[:120])
            package = page.request.get(SITE+"downloads/harbourlink-practice-project.zip",timeout=30000)
            assert package.status == 200, (label,package.status)
            assert package.body().startswith(b"PK"), (label,"invalid ZIP response")
            results["views"][label]={"websiteHttp":response.status,"appUrl":app.url,
                                      "appPageHasContent":True,"harbourlinkHttp":package.status,
                                      "twoVideos":True,"entryClick":"PASS"}
            context.close()
    finally:
        browser.close()
OUT.write_text(json.dumps(results,indent=2)+"\n",encoding="utf-8")
print("hosted-commercial-to-private-app-browser-journey: PASS")
print(json.dumps(results,indent=2))
