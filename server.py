import asyncio
from aiohttp import web
from socketio import AsyncServer

import client
from helpers import random_string

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


@server.on("download_youtube_video")
async def download_youtube_video(sid, data):
    to_emit = {"good": None, "result": None}
    filename = random_string()

    proc = await asyncio.create_subprocess_shell(
        f'ffmpeg -y -i "$(youtube-dl -x -g "{data["url"]}")" -f s16le -ac 2 -ar 48000 -acodec pcm_s16le {filename}.raw',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    await proc.communicate()

    to_emit["result"] = {
        "returncode": proc.returncode,
        "filename": f"{filename}.raw"
    }

    await server.emit("download_youtube_video", to_emit, sid)
