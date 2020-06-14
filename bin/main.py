import asyncio
import logging
import discord
import socket
import importlib

import concurrent.futures

import parse
import EventActions
# from parse import Chat, PayloadType, Commands
from terminal import Terminal as TerminalFull

import config

parser = parse.Chat()

class Terminal(TerminalFull):
    prompt = ""
    cmdqueue = False
    file = None

    def do_reload(self, arg):
        global parser
        importlib.reload(parse)
        parser = parse.Chat()
        print("Parser reloaded")


logging.basicConfig(level=logging.ERROR)

client = discord.Client()
term = Terminal(client)


@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Visitor")
    await member.add_roles(role)


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
