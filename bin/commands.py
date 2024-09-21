from inspect import getmembers, isfunction, getdoc
import discord
import re
import datetime

import logging
log = logging.getLogger(__name__)

class Commands:
    @staticmethod
    async def ping(client, cmd, args, message: discord.Message):
        """!Usage: {cmdChar}ping\nUsed to check if alive."""
        log.debug(message.created_at.time())
        if args:
            await message.channel.send(f"pong {args}")
        else:
            await message.channel.send(
                f"pong {message.created_at.replace(tzinfo=None).timestamp() - datetime.datetime.now().replace(tzinfo=None).timestamp()}"
            )
        return

    @staticmethod
    async def help(client, cmd, args, message):
        """Display available commands"""
        func_list = [o for o in getmembers(Commands) if isfunction(o[1])]
        help_text = ""
        if args:
            if " " in args:
                help_text = "Invalid search"
            else:
                for f in func_list:
                    if args.lower() == f[0] and getdoc(f[1]):
                        help_text = "Usage for {0}{1}: \n".format(Chat.cmdChar, args)
                        help_text += getdoc(f[1]).format(cmdChar=Chat.cmdChar)
                if not help_text:
                    help_text = "No help available for '{0}'".format(args)
        else:
            help_text = "Currently implemented commands: \n"
            for f in func_list:
                if getdoc(f[1])[0] == "!":
                    continue
                else:
                    help_text += Chat.cmdChar + f[0] + " "

            help_text += "\nFor more info, try {0}help [command]".format(Chat.cmdChar)
        await message.channel.send(help_text)


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
        log.info(f"args:{args}")
        e = discord.Embed()
        user = ""
        url = ""

        if args == "":
            user = message.author.display_name
            url = message.author.display_avatar.url
        else:
            for member in message.guild.members:
                if args.lower() == member.display_name.lower():
                    user = args
                    url = member.display_avatar.url
                    break

        e.set_author(name=user).set_image(url=url)
        message.channel.typing()
        await message.channel.send(embed=e)


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
            if any(ele in msg for ele in Passives.link_filters):
                await Passives.filter(message)
        except Exception as e:
            print(e)
            print(f"unhandled error in filter from '{msg}'")
            return
        try:
            if msg[0] != self.cmdChar:
                return
        except Exception as e:
            print(e)
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


class Passives:
    link_filters = [
        "twitter.com",
        "x.com",
    ]



    @staticmethod
    async def filter(message: discord.message):
        msg: str = message.content
        if msg.find("https://vxtwitter") or msg.find("http://vxtwitter"):
            return
        res = re.sub("(http(s)?://)(twitter|x)\\.com", "https://fixupx.com", msg)
        await message.edit(suppress=True)
        print(res)
        #await message.channel.send(message.author.mention + " " +res, flags=4096)
        await message.reply(res, mention_author=False)