import sqlite3
from typing import Tuple


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class DBHelp:

    def __init__(self, db_type: str, db_conn, db_table: str):
        self.db_type = db_type
        self.db_conn = db_conn
        self.db_table = db_table

    def sqlite_execute(self, sql, tup=None):

        conn = sqlite3.connect(self.db_conn)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute(sql, (tup, ))
        conn.commit()
        r = cur.fetchone()
        cur.close()
        conn.close()

        return r

    def sql_get(self, what='*', where: Tuple[str, str] = None):
        r = None
        if self.db_type == 'sqlite':
            self.db_conn: sqlite3.dbapi2.Connection = self.db_conn
            sql = f"SELECT {what} FROM `{self.db_table}`"
            if where:
                sql += f"WHERE {where[0]}=?"

            r = self.sqlite_execute(sql, where[1])

        return r

    def sql_insert(self):
        pass
