from __future__ import print_function
from peewee import *
from datetime import date

db_deffered = SqliteDatabase(None)

class BaseModel(Model):
    class Meta:
        database = db_deffered


class Tariff(BaseModel):
    name = CharField(unique=True)
    cpu = IntegerField()
    disk = IntegerField()
    ram = IntegerField()
    io = IntegerField()
    is_active = BooleanField(default=True)


class User(BaseModel):
    name = CharField(unique=True)
    password = CharField()
    default_password = CharField()
    domain = CharField()
    email = CharField()
    tariff_ = ForeignKeyField(Tariff, related_name="tariffs")
    is_active = BooleanField(default=True)
    created_date = DateField(default=date.today())
    server = CharField()


class Jet9DBError(Exception):
    pass


class Jet9DB(object):
    """Jet9 main DB management class"""

    def __init__(self, db_name=None):
        """Constructor"""

        if db_name is None:
            # we use it in development mode
            db_deffered.init(":memory:")
            self._create_tables()
        else:
            db_deffered.init(db_name)

        self.db = db_deffered


    def _create_tables(self, dbname=None):
        """Create tables from ORM"""

        # TODO: custom dbname creation
        Tariff.create_table()
        User.create_table()


    def _list_tables(self):
        """List all tables in DB"""

        return self.db.execute_sql("SELECT name FROM my_db.sqlite_master WHERE type='table';")


    def get_users(self, username=None):
        """Get user(s) from db"""

        if username is None:
            return User.select().order_by(User.name.asc())
        else:
            return User.select().where(User.name == username).order_by(User.name.asc())


    def get_tariffs(self, tariff=None):
        """Get tariff(s) from db"""

        if tariff is None:
            return Tariff.select()
        else:
            return Tariff.select().where(Tariff.name == tariff)


    def add_tariff(self, name, cpu, disk, ram, io, is_active=True):
        """Add tariff to DB"""

        return Tariff.create(name=name, cpu=cpu, disk=disk, ram=ram, io=io, is_active=is_active)


    def add_user(self, name, password, domain, email, tariff_name, server, created_date=None, is_active=True):
        """Add user to DB"""

        try:
            tariff = Tariff.select().where(Tariff.name == tariff_name).get()
        except Exception:
            raise Jet9DBError("Tariff {0} doesn't exists!".format(tariff_name))

        if created_date is None:
            created_date = date.today()

        return User.create(name=name, password=password, default_password=password,
            domain=domain, email=email, tariff_=tariff,
            server=server, created_date=created_date, is_active=is_active)

if __name__ == "__main__":

    #j = Jet9DB("j9db.sqlite")
    j = Jet9DB()

    j.add_tariff(name="m1.small", cpu=100, disk=1000, ram=2048, io=100, is_active=True)
    j.add_tariff(name="m1.medium", cpu=200, disk=2000, ram=4048, io=200, is_active=True)
    j.add_user( name="u1000", 
                password="secret",
                domain="u1000.jet9.29ah.ru", 
                email="u1000@jet9.29ah.ru", 
                tariff_name="m1.small",
                server="be01"
                )
    j.add_user( name="u1001", 
                password="secret2",
                domain="u1001.jet9.29ah.ru", 
                email="u1001@jet9.29ah.ru", 
                tariff_name="m1.medium",
                server="be01"
                )

    for u in j.get_users():
        print(u.name, u.tariff_.name)

    """
    Tariff.create_table()
    User.create_table()

    t = Tariff.create(name="m1.small", cpu=100, disk=1000, ram=2048, io=100, is_active=True)

    u = User.create(name="u1000", password="secret", default_password="secret",
                domain="u1000.jet9.29ah.ru", email="u1000@jet9.29ah.ru", tariffs_id=t,
                server="be01")
    u = User.create(name="u1001", password="secret", default_password="secret",
                domain="u1001.jet9.29ah.ru", email="u1001@jet9.29ah.ru", tariffs_id=t,
                created_date=date.today(), server="be02")

    for user in User.select().join(Tariff).where(Tariff.name == 'm1.small'):
        print user.name, user.tariffs_id.name, user.created_date
    """
