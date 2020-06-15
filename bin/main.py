import asyncio
import logging
import discord
import socket
import importlib

import concurrent.futures

import parse
import EventActions
# from parse import Chat, PayloadType, Commands
import terminal

import config

parser = parse.Chat()

class Terminal(terminal.Terminal):
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
    channel = next((channel for channel in member.guild.channels if channel.name == 'general'), None)
    await channel.send(f"""Welcome {member.mention} !   If you do not 
mind, could we have you type in your Player ID under the 
#playerid-room.  From there, one of us will invite you in game if 
we have not done so already! :slight_smile:  optionally, if or when 
you feel comfortable, we have an #introduction  page that you can 
use to break the ice with us and see your fellow Alliance members! 
:slight_smile:  Enjoy!""")
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
