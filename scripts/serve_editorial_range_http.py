"""Local static server with HTTP byte-range support for actual MP4 seeking tests."""
from pathlib import Path
from aiohttp import web

ROOT = Path(__file__).resolve().parents[1] / "docs"

async def homepage(request):
    return web.FileResponse(ROOT / "index.html")

app = web.Application()
app.router.add_get("/", homepage)
app.router.add_static("/", path=str(ROOT), show_index=False)
web.run_app(app, host="127.0.0.1", port=8000)
