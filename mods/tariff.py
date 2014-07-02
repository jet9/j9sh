from __future__ import print_function
from j9db import Jet9DB

class Jet9CmdTariff(object):
    def __init__(self):
        """Constructor"""

        self.db = None

    @staticmethod
    def cmd_path():
        """ Returns cmd path pattern """

        return {
            "tariff:Tariff management": {
                "list:Show list of tariffs": [],
                "show:Show tariff info": ["tariff"],
                "add:Add tariff to system": ["tariff", "cpu", "disk", "ram", "io"],
                "disable:Disable tariff in system": ["user"],
                "enable:Enable tariff in system": ["user"],
                "update:Update tariff to system": ["tariff", "cpu", "disk", "ram", "io"],
            },
        }

    def __connect_db(self):
        """Connect to DB"""

        self.db = Jet9DB("j9db.sqlite")
        return self.db


    def list(self, subcmd):
        """List all tariffs in DB"""

        self.__connect_db()
        tariffs = []

        for tariff in self.db.get_tariffs():
            tariffs.append(tariff.name)
            print(tariff.name)

        #print("\n".join(sorted(tariffs)))

    def add(self, subcmd, tariff, cpu, disk, ram, io):
        """Add tariff in DB"""

        self.__connect_db().add_tariff(name=tariff, cpu=cpu, disk=disk, ram=ram, io=io)


    def show(self, subcmd, tariff):
        """Show tariff info"""

        self.__connect_db()

        for t in self.db.get_tariffs(tariff=tariff):
            print("name:", t.name)
            print("cpu:", t.cpu)
            print("disk:", t.disk)
            print("ram:", t.ram)
            print("io:", t.io)
            print("active:", t.is_active)

    def enable(self, subcmd, user):
        """ info cmd routine """

        print("subcmd: {0} info: {1}".format(subcmd, user))

    def disable(self, subcmd, user):
        """ info cmd routine """

        print("subcmd: {0} info: {1}".format(subcmd, user))

# mapping for autoregister module in j9sh
mapping = { "tariff": Jet9CmdTariff }

