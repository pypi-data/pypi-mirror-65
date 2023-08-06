from __future__ import annotations
from typing import cast, Any
from typing_extensions import Protocol
from msql.cursor import Cursor


class Connection(Protocol):

    def cursor(self) -> Cursor:
        ...

    def close(self) -> None:
        ...

    def commit(self) -> None:
        ...

    def __enter__(self) -> Connection:
        ...

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        ...


# sadly we need to hold in memory connections
global_sqlite_memory_conn = None


def connection(conn_str: str) -> Connection:
    """
    Main factory that creates connections.
    Depending on connection string it will use library to create actual connection.

    :raises RuntimeError if unsupported DB type is used in connection string
    """

    def conn_sqlite() -> Connection:
        from sqlite3 import connect
        global global_sqlite_memory_conn

        # this transforms "sqlite://:memory:" => ":memory:"
        name = conn_str[len('sqlite://'):]

        conn = cast(Connection, connect(name))

        # if memory, we need to hold one connection
        if name == ":memory:":
            if global_sqlite_memory_conn is None:
                global_sqlite_memory_conn = conn
            return global_sqlite_memory_conn
        else:
            return conn

    def conn_postgres() -> Connection:
        from psycopg2 import connect
        return cast(Connection, connect(conn_str))

    def conn_unknown() -> Connection:
        raise RuntimeError("Unsupported DB type in connection string")

    switcher = {"sqlite": conn_sqlite, "postgres": conn_postgres}
    db_type = conn_str.split(':')[0]

    return switcher.get(db_type, conn_unknown)()
