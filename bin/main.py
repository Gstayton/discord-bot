import discord
import asyncio
import logging

from parser import Chat, Payload, PayloadType, Commands
import config

logging.basicConfig(level=logging.INFO)

client = discord.Client()
chat = Chat()

@client.event
async def on_ready():
    for server in client.servers:
        for role in server.roles:
            print(role)
    print("Logged in as \n {} \n {} \n------".format(client.user.name, client.user.id))
@client.event
async def on_message(message):
    print("{}: {}".format(message.author, message.content))
    if message.author == client.user.name:
        return
    else:
        payload = await chat.parse(client, message)

    if payload.payloadType == PayloadType.CHAT_MESSAGE:
        await client.send_message(message.channel, payload.response)

client.run(config.token)
