import cmd


class Terminal(cmd.Cmd):
    prompt = ">"
    cmdqueue = False
    file = None

    def __init__(self, client):
        cmd.Cmd.__init__(self)
        self.client = client

    def do_server(self, arg):
        for server in self.client.servers:
            print(server.name + "\n")

    def do_members(self, arg):
        for member in self.client.get_all_members():
            print("{} - {} : {}".format(member.server, member.name, member.id))

    def emptyline(self):
        print('')
