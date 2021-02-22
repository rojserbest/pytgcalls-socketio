from aiohttp import web
from socketio import AsyncServer

import client

app = web.Application()

server = AsyncServer()
server.attach(app)


@server.on("start")
async def start(sid, data):
    to_emit = {"good": None, "result": None}

    try:
        await client.start(**data)
        to_emit["good"] = True
        to_emit["result"] = True
    except Exception as e:
        to_emit["good"] = False
        to_emit["result"] = f"{type(e).__name__}: {e}"

    await server.emit("start", to_emit, sid)


@server.on("set_input")
async def set_input(sid, data):
    to_emit = {"good": None, "result": None}

    try:
        await client.set_input(**data)
        to_emit["good"] = True
        to_emit["result"] = True
    except Exception as e:
        to_emit["good"] = False
        to_emit["result"] = f"{type(e).__name__}: {e}"

    await server.emit("set_input", to_emit, sid)
