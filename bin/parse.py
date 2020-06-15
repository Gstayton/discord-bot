from inspect import getmembers, isfunction, getdoc
from enum import Enum
import discord
from decimal import *
import random


class Payload:
    def __init__(self, payloadType, response, target=None, status=0):
        self.__dict__.update({
            'Type': payloadType,
            'Response': response,
            'Target': target,
            'Status': status
        })
        self.status = status
        self.payloadType = payloadType
        self.response = response
        self.target = target


class PayloadType(Enum):
    CHAT_MESSAGE = 'chatmsg'
    SYS_MESSAGE  = 'sysmsg'
    NONE         = 'none'


class Commands:
    @staticmethod
    async def ping(client, cmd, args, message):
        "!Usage: {cmdChar}ping\nUsed to check if alive."
        await message.channel.send(f"pong {args}")
        return

    @staticmethod
    async def help(client, cmd, args, message):
        "!Display available commands"
        func_list = [o for o in getmembers(Commands) if isfunction(o[1])]
        helpText = ""
        if args:
            if " " in args:
                helpText = "Invalid search"
            else:
                for f in func_list:
                    if args.lower() == f[0] and getdoc(f[1]):
                        helpText = "Usage for {0}{1}: \n".format(Chat.cmdChar, args)
                        helpText += getdoc(f[1]).format(cmdChar=Chat.cmdChar)
                if not helpText:
                    helpText = "No help available for '{0}'".format(args)
        else:
            helpText = "Currently implemented commands: \n"
            for f in func_list:
                if getdoc(f[1])[0] == "!":
                    continue
                else:
                    helpText += Chat.cmdChar + f[0] + " "

            helpText += "\nFor more info, try {0}help [command]".format(Chat.cmdChar)
        await message.channel.send(helpText)


    @staticmethod
    async def about(client, cmd, args, message):
        """Information about this bot"""
        resp = """
This bot written and developed by Kosan Nicholas.\n
Source code available at https://github.com/Gstayton/discord-bot
        """

        await message.channel.send(resp)

    @staticmethod
    async def avatar(client, cmd, args, message):
        """Usage: {cmdChar}avatar <user>\nPosts users full size avatar\nLeave argument blank to fetch your own avatar"""
        print(f"args:{args}")
        e = discord.Embed()
        user = ""
        url = ""

        if args == "":
            user = message.author.display_name
            url = message.author.avatar_url
        else:
            for member in message.guild.members:
                print(member.display_name)
                if args == member.display_name:
                    print("Found")
                    user = args
                    url = member.avatar_url
                    break

        e.set_author(name=user).set_image(url=url)
        await message.channel.send(embed=e)


        print(message.author.display_name)
        for member in message.guild.members:
            print(member.display_name)
            if args == member.display_name:
                print("Found")
                e.set_author(name=args)
                e.set_image(url=member.avatar_url)
                await message.channel.send(message.author.mention, embed=e)
                return


class Chat:
    cmdChar = "."

    def __init__(self):
        self.commands = {}

        func_list = [o for o in getmembers(Commands) if isfunction(o[1])]

        for func in func_list:
            self.commands[func[0]] = func[1]

    async def parse(self, client, message):
        msg = message.content
        try:
            if msg[0] != self.cmdChar:
                return
        except:
            print(f"unhandled error from '{msg}'")
            return
        if " " in msg:
            cmd = msg[1:msg.find(" ")]
            args = msg[msg.find(" ") + 1:]
        else:
            cmd = msg[1:]
            args = ""
        if cmd in self.commands:
            return await self.commands[cmd](client, cmd, args, message)
        return
