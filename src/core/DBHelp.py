import sqlite3
from typing import Tuple, NoReturn


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class DBHelp:

    def __init__(self, db_object):
        self.db_type = db_object['raw']['type'].lower()
        self.db_conn = db_object['conn']
        self.db_table = db_object['raw']['table']

    def sqlite_execute(self, sql, tup=()):

        if not isinstance(tup, tuple):
            tup = (tup, )

        conn = sqlite3.connect(self.db_conn)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute(sql, tup)
        conn.commit()
        r = cur.fetchone()
        cur.close()
        conn.close()

        return r

    def sql_get(self, what='*', where: Tuple[str, str] = None, table: str = None):
        if table is None:
            table = self.db_table

        r = None
        if self.db_type == 'sqlite':
            sql = f"SELECT {what} FROM `{table}`"
            if where:
                sql += f" WHERE {where[0]}=?"

            r = self.sqlite_execute(sql, where[1])

        return r

    def sql_insert(self, keys: tuple, values: tuple, table: str = None) -> NoReturn:
        if table is None:
            table = self.db_table

        if self.db_type == 'sqlite':
            sql = f"INSERT INTO `{table}` {keys} VALUES ({'?, '.join('' for _ in values)+'?'})"
            self.sqlite_execute(sql, values)

    def sql_update(self, what, where, table: str = None):
        if table is None:
            table = self.db_table

        if self.db_type == 'sqlite':
            sql = f"UPDATE `{table}` SET {what} WHERE {where}"
            self.sqlite_execute(sql)
