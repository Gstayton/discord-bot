from inspect import getmembers, isfunction, getdoc
import discord

import db



class Commands:
    @staticmethod
    async def ping(client, cmd, args, message):
        """!Usage: {cmdChar}ping\nUsed to check if alive."""
        await message.channel.send(f"pong {args}")
        return

    @staticmethod
    async def playerid(client: discord.Client, cmd, args, message: discord.Message):
        """Register new playerid"""
        if args == "":
            await message.channel.send("Request must include a playerid")
            return

        q = db.get_session().query(db.PSO2User.user_id).filter(db.PSO2User.user_id==message.author.id)
        if db.session.query(q.exists()).scalar():
            await message.channel.send("User already registered")  # TODO: Add method to update user information
            return
        print(message.author.display_name)
        db.get_session().add(db.PSO2User(
            user_id=message.author.id,
            username=f"{message.author.name}#{message.author.discriminator}",
            player_id=args
        ))
        db.get_session().commit()

    @staticmethod
    async def query_playerid(client, cmd, args, message: discord.Message):
        """!nope"""
        s = db.get_session()
        r = s.query(db.PSO2User).filter_by(player_id=args).first()
        print(r)
        await message.channel.send(r)

    @staticmethod
    async def get_nonmembers(client: discord.Client, cmd, args, message: discord.Message):
        """!Return users with a registered playerid, but still in the visitor role"""
        s = db.get_session()
        members = message.guild.members
        users = []
        v_role = discord.utils.get(message.guild.roles, name="Visitor")
        for member in members:
            r = s.query(db.PSO2User).filter_by(user_id=member.id).first()
            if r is None:
                continue
            elif v_role in member.roles:
                users.append(r)
        await message.channel.send(f"Player_IDs: {[u.player_id for u in users]}")


    @staticmethod
    async def help(client, cmd, args, message):
        "!Display available commands"
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
        with message.channel.typing():
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
