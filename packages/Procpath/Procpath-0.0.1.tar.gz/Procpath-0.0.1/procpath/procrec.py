import sqlite3

from . import procfile


__all__ = 'SqliteStorage',


class SqliteStorage:

    _conn = None

    _file_list = None

    _file_columns = None

    def __init__(self, database: str, file_list):
        self._file_list = file_list

        self._conn = sqlite3.connect(database, isolation_level=None)

    def create_schema(self):
        table_columns = []
        self._file_columns = []
        for file_name in sorted(self._file_list):
            schema = procfile.registry[file_name].schema
            if isinstance(schema, str):
                table_columns.append(f'{file_name} TEXT')
                self._file_columns.append(file_name)
            else:
                for field_name, field_type in schema._field_types.items():
                    column_name = f'{file_name}_{field_name}'
                    table_columns.append('{column} {type}'.format(
                        column=column_name, type={int: 'INTEGER', str: 'TEXT'}[field_type]
                    ))
                    self._file_columns.append(column_name)

        sql = '''
            CREATE TABLE IF NOT EXISTS record (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                ts        DATETIME DEFAULT(STRFTIME('%Y-%m-%dT%H:%M:%f', 'NOW')),
                {columns}
            )
        '''.format(columns=',\n'.join(table_columns))
        self._conn.execute(sql)

    def record(self, node_list):
        assert node_list and 'stat_pid' in node_list[0], 'Malformed process tree node'

        sql = 'INSERT INTO record({columns}) VALUES({placeholders})'.format(
            columns=','.join(self._file_columns),
            placeholders=','.join(f':{c}' for c in self._file_columns)
        )
        self._conn.executemany(sql, node_list)

    def close(self):
        self._conn.close()

    def __enter__(self):
        self.create_schema()
        return self

    def __exit__(self, *exc_args):
        self.close()
