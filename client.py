from typing import Union

from pyrogram import Client
from pytgcalls import GroupCall

from config import SESSION_NAME, API_ID, API_HASH


client = Client(SESSION_NAME, API_ID, API_HASH)
client.start()

pytgcalls = GroupCall(client)


async def start(group: Union[str, int]) -> None:
    await pytgcalls.start(group)


async def mute(muted: bool) -> None:
    await pytgcalls.set_is_mute(muted)


def set_input(file: str) -> None:
    pytgcalls.input_filename = file


def set_output(file: str) -> None:
    pytgcalls.output_filename = file
