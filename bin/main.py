import asyncio
import logging
import discord
import socket
import importlib

import concurrent.futures

import commands
import EventActions
import terminal

import config

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


logging.basicConfig(level=logging.ERROR)

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
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        await parser.parse(client, message)


async def main(loop):
    try:
        await client.start(config.TOKEN)
    except socket.timeout:
        loop.create_task(main(loop))
        return


if __name__ == "__main__":
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))
    loop.run_in_executor(executor, term.cmdloop)
    loop.run_forever()
