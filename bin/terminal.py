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
