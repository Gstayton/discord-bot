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

client = discord.Client()
term = Terminal(client)


@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Visitor")
    channel = next((channel for channel in member.guild.text_channels if channel.name == 'general'), None)
    linkable = next((channel for channel in member.guild.text_channels if channel.name == "playerid-room"))
    await channel.send(f"""Welcome {member.mention} ! Feel free to chat with other members, and if you'd like to
join, simple head on over to {discord.utils.get(member.guild.text_channels, name='bot-chat').mention}, where you
can register your player-id with .playerid [player-id] !""")
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
