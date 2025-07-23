from DB.tables.users import UsersTable
from DB.tables.queries import QueriesTable


def init_database():
    with UsersTable() as users_db:
        users_db.create_table()

    with QueriesTable() as queries_db:
        queries_db.create_table()
