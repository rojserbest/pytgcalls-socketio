import sys

from socketio import Client as SocketIOClient
from pyrogram import (
    Client as TelegramClient, client,
    filters
)
from pyrogram.types import Message
from socketio.client import Client

from config import (SESSION2_NAME, API_ID, API_HASH, HOST, PORT)


socketio = SocketIOClient()
telegram = TelegramClient(SESSION2_NAME, API_ID, API_HASH)


@telegram.on_message(filters.command("start", ">") & filters.me)
def start(client: Client, message: Message):
    socketio.emit("start", {"group": message.chat.id})

    @socketio.on("start")
    def start(data):
        message.edit_text(str(data))


@telegram.on_message(filters.command("youtube", ">") & filters.me)
def youtube(client: Client, message: Message):
    socketio.emit(
        "download_youtube_video", {
            "url": message.reply_to_message.text
        }
    )

    @socketio.on("download_youtube_video")
    def download_youtube_video(data):
        message.edit_text(str(data))


@telegram.on_message(filters.command("input", ">") & filters.me)
def input(client: Client, message: Message):
    socketio.emit(
        "set_input", {
            "file": message.command[1]
        }
    )

    @socketio.on("set_input")
    def set_input(data):
        message.edit_text(str(data))


socketio.connect(f"http://{HOST}:{PORT}")
telegram.run()
