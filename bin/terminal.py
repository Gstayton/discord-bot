import cmd

import db

class Terminal(cmd.Cmd):
    prompt = ""
    cmdqueue = False
    file = None

    def __init__(self, client):
        cmd.Cmd.__init__(self)
        self.client = client

    def do_servers(self, arg):
        for server in self.client.guilds:
            print(server.name)

    def do_members(self, arg):
        for member in self.client.get_all_members():
            print("{} - {} : {}".format(member.guild, member.name, member.id))

    def do_geticons(self, arg):
        for member in self.client.get_all_members():
            print(member.avatar)
            print(member.avatar == None)

    def emptyline(self):
        print('')
