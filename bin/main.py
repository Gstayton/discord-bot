import asyncio
import logging
import discord

import concurrent.futures

from parser import Chat, Payload, PayloadType, Commands
from terminal import Terminal
import config

logging.basicConfig(level=logging.INFO)

client = discord.Client()
term = Terminal(client)

@client.event
async def on_ready(self):
    for server in client.servers:
        print(server.id)
    print("Logged in as \n {} \n {} \n------".format(client.user.name, client.user.id))
@client.event
async def on_message(self, message):
    print("{}: {}".format(message.author, message.content))
    if message.author == client.user.name:
        return
    else:
        payload = await self.parser.parse(client, message)

    if payload.payloadType == PayloadType.CHAT_MESSAGE:
        await client.send_message(message.channel, payload.response)

async def main():
    await client.start(config.token)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
loop = asyncio.get_event_loop()
loop.create_task(client.start(config.token))
loop.run_in_executor(executor, term.cmdloop)
loop.run_forever()
