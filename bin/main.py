import asyncio
import discord
import socket
import importlib
import os

import concurrent.futures

import commands
import terminal

import config

import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger()

parser = commands.Chat()

class Terminal(terminal.Terminal):
    prompt = ""
    cmdqueue = False
    file = None

    def do_reload(self, arg):
        global parser
        importlib.reload(commands)
        parser = commands.Chat()
        print("Parser reloaded")


intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.typing = True
client = discord.Client(intents=intents)
term = Terminal(client)


@client.event
async def on_member_join(member):
    pass


@client.event
async def on_ready():
    log.info(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        await parser.parse(client, message)


async def main():
    try:
        await client.start(config.TOKEN)
    except socket.timeout:
        await asyncio.create_task(main())
        return


if __name__ == "__main__":
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_in_executor(executor, term.cmdloop)
    asyncio.run(main())