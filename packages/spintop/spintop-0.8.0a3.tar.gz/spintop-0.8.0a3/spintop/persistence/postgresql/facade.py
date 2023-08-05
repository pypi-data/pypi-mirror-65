import os

from spintop.persistence import PersistenceFacade
from spintop.models import (
    SpintopTestRecord, 
    SpintopSerializedFlatTestRecord, 
    SpintopSerializedTestRecordCollection, 
    TestRecordSummary,
    Query, 
    serialized_get_test_uuid,
    get_json_serializer
)

from spintop.errors import SpintopException

from .models import SQLTestRecord
from .operations import engine_from_uri, SQLOperations
from .queryset import PostgreSQLQuery

class PostgreSQLPersistenceFacade(PersistenceFacade):
    def __init__(self, sql_engine):
        self.sql_ops = SQLOperations(sql_engine)
        self.serializer = get_json_serializer(datetime_serializer=lambda datetime_obj: datetime_obj.timestamp())
        super().__init__(self.serializer)
        self.init()

    def init(self):
        self.sql_ops.create_tables()
    
    @classmethod
    def from_env(cls, uri, database_name, env=None):
        return cls(engine_from_uri(uri, database_name))
        
    def _create(self, records):
        records = self._to_sql_records(records)
        session = self.sql_ops.new_session()
        session.add_all(records)
        session.commit()
    
    def _to_sql_records(self, records):
        return [SQLTestRecord(test_uuid=record.test_uuid, data=record.as_dict()) for record in records]

    def count(self, query=None):
        if query is None: query = Query()
        session = self.sql_ops.new_session()
        operation = session.query(SQLTestRecord).filter(*self._to_filter(query))
        return operation.count()
    
    def avg_obj_size(self):
        raise NotImplementedError()
        
    def _retrieve(self, query=None, limit_range=None):
        """ Retrieve is responsible with returning the test_record (top level phase) associated
        with the matched features.
        """
        session = self.sql_ops.new_session()

        if query is None: query = Query()
        
        operation = session.query(SQLTestRecord).filter(*self._to_filter(query))
        if limit_range:
            operation = operation.offset(limit_range[0]).limit(limit_range[1] - limit_range[0])

        records = operation.all()
        records = [record.data for record in records]
        return SpintopSerializedTestRecordCollection(records)

    def _to_filter(self, query):
        return PostgreSQLQuery(query).build_data_query(SQLTestRecord)

    def _update(self, records, upsert=False):
        all_features = []
        test_uuids = []

        for record in records:
            all_features += record.all_features
            test_uuids += [record.test_uuid]

        session = self.sql_ops.new_session()

        session.query(SQLTestRecord).filter(*self._to_filter(Query().test_uuid_any_of(test_uuids))).delete(synchronize_session='fetch')
        records = self._to_sql_records(records)
        session.add_all(records)
        session.commit()
    
    def _delete(self, match_query):
        session = self.sql_ops.new_session()
        session.query(SQLTestRecord).filter(*self._to_filter(match_query)).delete(synchronize_session='fetch')
        session.commit()