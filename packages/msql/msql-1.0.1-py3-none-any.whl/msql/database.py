from __future__ import annotations

from typing import Any

from msql.cursor import Cursor
from msql.connection import Connection, connection
from msql.migration_tool import MigrationTool


class _ContextHelper:

    def __init__(self, db: Database):
        self.db = db

    def __enter__(self) -> Cursor:
        self.conn = self.db.connection()
        return self.conn.cursor()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self.db.auto_commit:
            self.conn.commit()


class Database:

    def __init__(self,
                 conn_str: str,
                 migration_dir: str,
                 schema_table: str = "msql_migration",
                 auto_commit: bool = True) -> None:
        self.conn_str = conn_str
        self.migration_tool = MigrationTool(conn_str, migration_dir, schema_table)
        self.auto_commit = auto_commit

    def migrate(self) -> None:
        self.migration_tool.install()
        self.migration_tool.apply_migrations()

    def connection(self) -> Connection:
        return connection(self.conn_str)

    def get_cursor(self) -> _ContextHelper:
        return _ContextHelper(self)
