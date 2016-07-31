from inspect import getmembers, isfunction, getdoc
from enum import Enum
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


class Commands():
    @staticmethod
    async def ping(client, cmd, args, message):
        "Usage: {cmdChar}ping\nUsed to check if alive."
        return Payload(
            PayloadType.CHAT_MESSAGE,
            "pong {}".format(args)
        )

    @staticmethod
    async def help(client, cmd, args, message):
        "Display available commands"
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
                helpText += Chat.cmdChar + f[0] + ", "

            helpText += "\nFor more info, try {0}help [command]".format(Chat.cmdChar)
        return Payload(
            PayloadType.CHAT_MESSAGE,
            helpText
            )

    async def about(client, cmd, args, message):
        "Information about this bot"
        resp = """
This bot written and developed by Kosan Nicholas.\n
Source code available at https://github.com/Gstayton/discord-bot
        """

        return Payload(
            PayloadType.CHAT_MESSAGE,
            resp
        )

    @staticmethod
    async def set_role(client, cmd, args, message):
        "Usage: {cmdChar}set_role <role>\nSet yourself to the selected role. Only certain roles on the server are allowed."
        whitelist = [
            'Ami',
            'Taiga',
            'Minorin',
            'Inko',
            'Kitamura',
            'Ryuuji'
        ]
        roles = message.server.roles
        for role in roles:
            if role.name == args and role.name in whitelist:
                target = role
        if args == "":
            return Payload(
                PayloadType.CHAT_MESSAGE,
                "Available roles: {0}".format(", ".join(whitelist))
            )
        elif args in whitelist:
            await client.remove_roles(message.author, *whitelist)
            await client.add_roles(message.author, target)
            return Payload(
                PayloadType.CHAT_MESSAGE,
                "Role set to {}.".format(args)
            )
        else:
            return Payload(
                PayloadType.CHAT_MESSAGE,
                "Selected role not available"
            )



class Chat():
    cmdChar = "."

    def __init__(self):
        self.commands = {}

        func_list = [o for o in getmembers(Commands) if isfunction(o[1])]

        for func in func_list:
            self.commands[func[0]] = func[1]

    async def parse(self, client, message):
        msg = message.content
        if msg[0] != self.cmdChar:
            return Payload(
                1,
                PayloadType.NONE,
                None
                )
        if " " in msg:
            cmd = msg[1:msg.find(" ")]
            args = msg[msg.find(" ") + 1:]
        else:
            cmd = msg[1:]
            args = ""
        print("COMMAND : " + cmd)
        if cmd in self.commands:
            return await self.commands[cmd](client, cmd, args, message)
        else:
            return Payload(
                    1,
                    PayloadType.NONE,
                    None
                    )
