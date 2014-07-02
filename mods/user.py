from __future__ import print_function
from j9db import Jet9DB

class Jet9CmdUser(object):
    def __init__(self):
        """Constructor: returns pattern for commands"""

        self.db = None

    @staticmethod
    def cmd_path():
        """ Returns cmd path pattern """

        return {
            "user:User management": {
                "show:Show user info": ["user"],
                "list:Show list of users": [],
                "add:Add user to system": ["user", "password", "email", "domain", "tariff", "server"],
                "disable:Disable user in system": ["user"],
                "enable:Enable user in system": ["user"],
                "remove:Remove user from system": ["user"],
                "set_password:": {
                    "main:Set main system passwd for user": [ "user", "password" ],
                    "lcx_root:Set lxc root password for user": [ "user", "password" ],
                },
                "set_tariff:Set user's tariff": [ "user", "tariff" ],
            },
        }

    def __connect_db(self):
        """Connect to DB"""

        self.db = Jet9DB("j9db.sqlite")
        return self.db


    def list(self, subcmd):
        """List all users in DB"""

        self.__connect_db()

        for user in self.db.get_users():
            print(user.name)

    def add(self, subcmd, user, password, email, domain, tariff, server):
        """Add user in DB"""

        self.__connect_db().add_user(name=user, password=password,
                    email=email, domain=domain, tariff_name=tariff, server=server)

        #TODO: add user on remote system


    def show(self, subcmd, user):
        """Show user details"""

        self.__connect_db()

        for user in self.db.get_users(user):
            print("name:", user.name)
            print("password:", user.password)
            print("default_password:", user.default_password)
            print("domain:", user.domain)
            print("email:", user.email)
            print("tariff:", user.tariff_.name)
            print("server:", user.server)
            print("active:", user.is_active)

    def enable(self, subcmd, user):
        """ info cmd routine """

        print("subcmd: {0} info: {1}".format(subcmd, user))

    def disable(self, subcmd, user):
        """ info cmd routine """

        print("subcmd: {0} info: {1}".format(subcmd, user))

# mapping for autoregister module in j9sh
mapping = { "user": Jet9CmdUser }

