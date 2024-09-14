import cmd

import logging
log = logging.getLogger(__name__)


class Terminal(cmd.Cmd):
    prompt = ""
    cmdqueue = False
    file = None

    def __init__(self, client):
        cmd.Cmd.__init__(self)
        self.client = client

    def do_servers(self, arg):
        for guild in self.client.guilds:
            print(f"{guild.name} - {guild.id} - {guild.member_count}\n{[guild.name for guild in guild.roles]}")

    def do_members(self, arg):
        for member in self.client.get_all_members():
            print("{} - {} : {}".format(member.guild, member.name, member.id))

    def do_geticons(self, arg):
        for member in self.client.get_all_members():
            print(member.avatar)
            print(member.avatar is None)

    def emptyline(self):
        print('')
