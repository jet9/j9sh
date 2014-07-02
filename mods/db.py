from __future__ import print_function
import sys

from j9db import Jet9DB

def query_yes_no(question, default="no"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")


class Jet9CmdDB(object):
    def __init__(self):
        """Constructor: returns pattern for commands"""

        self.db = None

        pass

    @staticmethod
    def cmd_path():
        """ Returns cmd path pattern """

        # ALWAYS BE SURE TO ADD ":" TO THE END OF KEY WITHOUT HELP STRING
        return {
            "db:Low-level database management": {
                "create:Create database": ["dbname"],
                "show:": {
                    "tables:Show tables": [],
                    "fields:Show fields in specific table": ["table"],
                    "data:Show table data": ["table"],
                },
            },
        }

    def __connect_db(self):
        """Connect to DB"""

        # MOVE TO CONFIG:
        self.db = Jet9DB("j9db.sqlite")


    def create(self, subcmd, dbname):
        """Create new database"""

        if query_yes_no("Are You really wants to create new db?", default="no"):
            self.__connect_db()
            self.db._create_tables(dbname)
            print("New empty DB created")
        else:
            print("Canceled")

    def show(self, subcmd, user):
        """Show information about DB"""

        print("XXX: subcmd: {0} info: {1}".format(subcmd, user))

# mapping for autoregister module in j9sh
# example:
# mapping = { "commandXXX": Jet9CmdXXX }
mapping = { "db": Jet9CmdDB }

