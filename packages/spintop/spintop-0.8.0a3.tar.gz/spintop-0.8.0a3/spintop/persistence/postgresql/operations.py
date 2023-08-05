import os

from sqlalchemy import create_engine, Table, MetaData, select, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoSuchTableError, ProgrammingError

from .models import Base

def engine_from_uri(uri, database_name=None):
    if database_name:
        uri = f'{uri}/{database_name}'
    return create_engine(uri)

class SQLOperations(object):
    def __init__(self, engine):
        self.engine = engine
        self.meta = MetaData(self.engine)
        self.Session = sessionmaker(engine)

    def new_session(self):
        return self.Session()

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def __getitem__(self, table_name):
        try:
            if not self.engine.dialect.has_table(self.engine, table_name):
                raise NoSuchTableError(table_name)
            
            return TableOperations(
                Table(table_name, self.meta, autoload=True, autoload_with=self.engine),
                self.engine
            )
        except (NoSuchTableError, ProgrammingError) as e:
            raise KeyError(str(e))

class TableOperations(object):
    def __init__(self, table, engine):
        self.table = table
        self.engine = engine
    
    def list_existing_indices(self, indices, column_name='index'):
        with self.engine.connect() as conn:
            rows = conn.execute(
                select(
                    [self.table.c[column_name]], 
                    self.table.c[column_name].in_(tuple(indices))
                )
            ).fetchall()

            return [row[0] for row in rows] # We requested only one field.

    def delete_indices(self, indices, column_name='index'):
        with self.engine.connect() as conn:
            conn.execute(
                delete(
                    self.table, 
                    self.table.c[column_name].in_(tuple(indices))
                )
            )

    def drop_table(self):
        self.table.drop()
        self.table.metadata.reflect()