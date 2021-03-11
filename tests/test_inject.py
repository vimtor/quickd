from quickd import inject, factory


class Database:
    pass


class PostgreSQL(Database):
    def __str__(self):
        return 'PostgreSQL'


class MySQL(Database):
    def __str__(self):
        return 'MySQL'


def test_constructor_inject():
    class UserService:
        @inject
        def __init__(self, database: Database):
            self.database = database

        def get_database(self):
            return str(self.database)

    @factory
    def choose_database() -> Database:
        return PostgreSQL()

    assert UserService().get_database() == 'PostgreSQL'
    assert UserService(MySQL()).get_database() == 'MySQL'


def test_function_inject():
    @inject
    def get_database(database: Database):
        return str(database)

    @factory
    def choose_database() -> Database:
        return PostgreSQL()

    assert get_database() == 'PostgreSQL'
    assert get_database(MySQL()) == 'MySQL'
