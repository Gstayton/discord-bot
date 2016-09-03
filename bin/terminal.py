import cmd

import db

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

    def do_adddb(self, arg):
        for server in self.client.servers:
            db.session.add(db.Server(
                server_id=server.id,
                server_name=server.name
            ))

    def do_adduser(self, arg):
        for user in self.client.get_all_members():
            server = db.session.query(db.Server).filter(db.Server.server_id == user.server.id).first()
            db.session.add(db.User(
                user_id = user.id,

            ))

    def emptyline(self):
        print('')
