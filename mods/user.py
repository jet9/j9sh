from __future__ import print_function
from j9db import Jet9DB, Jet9DBError

class Jet9CmdUser(object):
    def __init__(self):
        """Constructor: returns pattern for commands"""

        self.db = self.__connect_db()

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
        """List all users in Jet9 system"""

        for user in self.db.get_users():
            print(user.name)


    def add(self, subcmd, user, password, email, domain, tariff, server):
        """Add user to Jet9 system"""

        try:
            self.db.add_user(name=user, password=password,
                    email=email, domain=domain, tariff_name=tariff, server=server)

        except Jet9DBError as e:
            print("Add user failed: {0}".format(e))
            return 1


        #TODO: add user on remote system


    def show(self, subcmd, user):
        """Show user details"""

        for user in self.db.get_users(user):
            print("name:", user.name)
            print("password:", user.password)
            print("default_password:", user.default_password)
            print("domain:", user.domain)
            print("email:", user.email)
            print("tariff:", user.tariff_.name)
            print("server:", user.server)
            print("active:", user.is_active)


    def _toggle_user(self, user, enable=True):
        """Toggle user active state"""

        try:
            state = self.db.toggle_user(user, enable=enable)
            if state is None:
                print("No such user: {0}".format(user))
                return 1

        except Jet9DBError as e:
            print("Enable user error: {0}".format(e))

        print("User enabled: {0}".format(state))


    def enable(self, subcmd, user):
        """Enable user in system"""

        return self._toggle_user(user, enable=True)


    def disable(self, subcmd, user):
        """Disable user in system"""

        return self._toggle_user(user, enable=False)


    def remove(self, subcmd, user):
        """Completely remove user from all systems"""
        try:
            for u in self.db.get_users(user):
                #remove user from backend server
                pass

            # remove user from db
            self.db.remove_user(user)

        except Jet9DBError as e:
            print("remove user error: {0}".format(e))


    def set_password(self, subcmd, user, password):
        """Set password for user"""

        if subcmd == "main":
            try:
                self.db.set_password(user, password)

            except Jet9DBError as e:
                print("set_password error: {0}".format(e))
                return 1
            # XXX: set password on remote system

        elif subcmd == "lxc_root":
            # XXX: set password for root@lxc on remote system
            pass


    def set_tariff(self, subcmd, user, tariff):
        """Change tariff for user"""

        try:
            self.db.set_tariff(user, tariff)

        except Jet9DBError as e:
            print("set_tariff error: {0}".format(e))
            return 1
        # XXX: set password on remote system



# mapping for autoregister module in j9sh
mapping = { "user": Jet9CmdUser }

