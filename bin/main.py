import asyncio
import logging
import discord

import concurrent.futures

from parser import Chat, Payload, PayloadType, Commands
from terminal import Terminal
import config

logging.basicConfig(level=logging.ERROR)

client = discord.Client()
term = Terminal(client)

parser = Chat()

@client.event
async def on_ready():
    pass

@client.event
async def on_message(message):
    if message.author == client.user.name:
        return
    else:
        payload = await parser.parse(client, message)

    if payload.payloadType == PayloadType.CHAT_MESSAGE:
        await client.send_message(message.channel, payload.response)

async def main():
    await client.start(config.token)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
loop = asyncio.get_event_loop()
loop.create_task(client.start(config.token))
loop.run_in_executor(executor, term.cmdloop)
loop.run_forever()
