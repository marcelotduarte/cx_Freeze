# server_simple.py
from __future__ import annotations

from aiohttp import web


async def handle(request):
    name = request.match_info.get("name", "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def wshandle(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            await ws.send_str(f"Hello, {msg.data}")
        elif msg.type == web.WSMsgType.BINARY:
            await ws.send_bytes(msg.data)
        elif msg.type == web.WSMsgType.CLOSE:
            break

    return ws


app = web.Application()
app.add_routes(
    [
        web.get("/", handle),
        web.get("/echo", wshandle),
        web.get("/{name}", handle),
    ]
)

web.run_app(app)
