from spintop.generators import Generator

from spintop.models import (
    SpintopSerializedFlatTestRecord,
    TestRecordSummary, 
    FeatureRecord, 
    SpintopTestRecord,
    Query
)

from spintop.utils import AnonymousGetRecursive


from ..logs import _logger
from ..errors import SpintopException, spintop_warn
from ..messages import NoopMessagePublisher, TestsUpdateMessage

logger = _logger('persistence')


class MissingMapper(SpintopException):
    def __init__(self, cls):
        super().__init__("Mapper for class {!r} is mandatory.".format(cls))

class NoMapperForObject(SpintopException):
    def __init__(self, obj, mappers):
        super(NoMapperForObject, self).__init__(
            'There are no known mapper able to interact with obj {!r} of class {}. Declared mappers are: {}'.format(
                obj,
                obj.__class__,
                [cls.__name__ for cls in mappers]
            )
        )
        
class DuplicateMapperClassName(SpintopException):
    def __init__(self, objcls):
        super(DuplicateMapperClassName, self).__init__(
            'The name of the class {} is duplicate. The class name linked to a mapper must be unique.'.format(
                objcls,
            )
        )

class TestRecordNotFound(SpintopException):
    def __init__(self, test_uuid):
        super().__init__(f'Test Record with UUID {test_uuid!r} not found.')

class ManyTestRecordFound(SpintopException):
    def __init__(self, test_uuid, count):
        super().__init__(f'{count} Test Records where found with UUID {test_uuid!r}, but only one was expected.')


class PersistenceFacade(object):
    logger = logger
    def __init__(self, serializer, messages=None):
        self.serializer = serializer

        if messages is None:
            # Will discard all messages
            messages = NoopMessagePublisher()

        self.messages = messages

    @classmethod
    def from_env(cls, uri, database_name, env=None):
        raise NotImplementedError()

    def _publish_test_record_update(self, test_records):
        modified_test_uuids = set(tr.test_uuid for tr in test_records)

        dut_id_field = TestRecordSummary.test_id.dut.id.name_

        modified_duts = set(AnonymousGetRecursive(tr.test_record).get_recursive(dut_id_field) for tr in test_records)

        self.messages.tests_update.publish(TestsUpdateMessage.create(
            updated_test_uuids=list(modified_test_uuids),
            affected_duts=list(modified_duts)
        ))

    def _publish_update_all(self):
        spintop_warn('Current update all deletes and re-creates all tests instead of targeting deleted uuids. This is very inefficient.')
        self.messages.tests_update.publish(TestsUpdateMessage.create(
            delete_all=True,
            update_all=True
        ))

    def serialize_barrier(self, records):
        records = list(records)
        if records and isinstance(records[0], SpintopTestRecord):
            records = [self.serializer.serialize(obj) for obj in records]

        if records and isinstance(records[0], dict):
            return [SpintopSerializedFlatTestRecord(**record) for record in records]
        else:
            return records

    def create(self, records):
        records = self.serialize_barrier(records)
        ret_val = self._create(records)
        self._publish_test_record_update(records)
        return ret_val

    def _create(self, records):
        raise NotImplementedError()
        
    def retrieve(self, query=None, deserialize=True, limit_range=None):
        if query is None: query = Query()
        serialized_collection = self._retrieve(query, limit_range=limit_range)
        if deserialize:
            yield from serialized_collection.deserialize(self.serializer)
        else:
            yield from (record for record in serialized_collection.records)

    def _retrieve(self, query, limit_range=None):
        """Should return a ``SpintopSerializedTestRecordCollection``"""
        raise NotImplementedError()
        
    def retrieve_one(self, test_uuid, deserialize=True):
        records = self.retrieve(Query().test_uuid_is(test_uuid), deserialize=deserialize)
        records = list(records)

        count = len(records)
        if count < 1:
            raise TestRecordNotFound(test_uuid)
        elif count > 1:
            raise ManyTestRecordFound(test_uuid, count)
        else:
            return records[0]
    
    def count(self, query=None):
        if query is None: query = Query()
        return self._count(query)
    
    def _count(self, query):
        raise NotImplementedError()

    def update(self, records, upsert=False):
        records = self.serialize_barrier(records)
        ret_val = self._update(records, upsert=upsert)
        self._publish_test_record_update(records)
        return ret_val

    def _update(self, records, upsert=False):
        raise NotImplementedError()
    
    def delete(self, query=None):
        if query is None: query = Query()
        ret_val = self._delete(query)
        self._publish_update_all()
        return ret_val

    def _delete(self, query=None):
        raise NotImplementedError()
    
    def create_records_generator(self):
        return PersistenceGenerator(self)
        
def create_mapper_name_index(mappers):
    mappers_name_index = {}
    for mapped_cls, mapper in mappers.items():
        name = mapped_cls.__name__
        if name in mappers_name_index:
            raise DuplicateMapperClassName(mapped_cls)
        mappers_name_index[name] = mapper
    return mappers_name_index
    
class PersistenceGenerator(Generator):
    def __init__(self, facade):
        super().__init__()
        self.facade = facade
    
    def __call__(self, *args, **kwargs):
        return self.facade.retrieve(*args, **kwargs)

class Mapper(object):
    def init(self):
        pass