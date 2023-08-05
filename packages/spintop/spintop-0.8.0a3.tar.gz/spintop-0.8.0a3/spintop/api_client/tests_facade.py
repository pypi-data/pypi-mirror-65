from datetime import datetime

from spintop.persistence.base import PersistenceFacade

from ..models import SpintopSerializedTestRecordCollection, Query, get_json_serializer, SpintopTestRecord

from .schemas import tests_schema, test_count_schema

class SpintopAPIPersistenceFacade(PersistenceFacade):
    def __init__(self, spintop_api):
        self.spintop_api = spintop_api
        self.serializer = get_json_serializer()
        super().__init__(self.serializer)

    @classmethod
    def from_env(self, uri, database_name=None, env=None):
        # database_name is the org_id
        api = env.spintop_factory()
        return api.tests

    @property
    def session(self):
        return self.spintop_api.session

    def _create(self, records):
        serialized = self._records_in_schema(records)
        return self.session.post(self.spintop_api.get_link('tests.create'), json=serialized)
        
    def _records_in_schema(self, records):
        return tests_schema.dump({'tests': [record.as_dict() for record in records]})

    def _retrieve(self, query, limit_range=None):
        query_dict = query.as_dict()
        if limit_range:
            query_dict['limit_range_inf'] = limit_range[0]
            query_dict['limit_range_sup'] = limit_range[1]

        resp = self.session.get(self.spintop_api.get_link('tests.retrieve'), params=query_dict)
        tests = tests_schema.load(resp.json())['tests']
        return SpintopSerializedTestRecordCollection(tests)

    # def retrieve_one(self, test_uuid):
    #     resp = self.session.get(self.spintop_api.get_link('tests.retrieve_one', test_uuid=test_uuid))
    #     test = resp.json()
    #     return get_json_serializer().deserialize(SpintopTestRecord, test)
        
    def _count(self, query):
        query_dict = query.as_dict()
        resp = self.session.get(self.spintop_api.get_link('tests.count'), params=query_dict)
        return test_count_schema.load(resp.json())['count']

    def _update(self, records, upsert=True):
        serialized = self._records_in_schema(records)
        return self.session.put(self.spintop_api.get_link('tests.update'), json=serialized)
    
    def _delete(self, query):
        query_dict = query.as_dict()
        return self.session.delete(self.spintop_api.get_link('tests.delete'), params=query_dict)