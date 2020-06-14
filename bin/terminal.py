import cmd

import db

class Terminal(cmd.Cmd):
    prompt = ""
    cmdqueue = False
    file = None

    def __init__(self, client):
        cmd.Cmd.__init__(self)
        self.client = client

    def do_server(self, arg):
        for server in self.client.servers:
            print(server.name)

    def do_members(self, arg):
        for member in self.client.get_all_members():
            print("{} - {} : {}".format(member.server, member.name, member.id))

    def do_addservers(self, arg):
        for server in self.client.servers:
            db.session.add(db.Server(
                server_id=server.id,
                name=server.name
            ))
        db.session.commit()

    def do_addusers(self, arg):
        for user in self.client.get_all_members():
            db.session.add(db.User(
                user_id=user.id,
                username=user.name,
                server_id=user.server.id
            ))
        print('finished')
        db.session.commit()

    def do_dbflush(self, arg):
        db.session.flush()

    def do_geticons(self, arg):
        for member in self.client.get_all_members():
            print(member.avatar)
            print(member.avatar == None)

    def emptyline(self):
        print('')
