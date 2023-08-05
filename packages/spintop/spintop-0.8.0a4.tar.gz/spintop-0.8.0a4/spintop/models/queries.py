import re
from functools import wraps
from collections import OrderedDict, defaultdict
from .test_records import FeatureRecord, TestRecordSummary
from .serialization import get_json_serializer


from spintop.utils.dict_ops import (
    update,
    deepen_dict,
    flatten_dict
)

def record_call(exclude_top_level=False):
    def _record_call(fn):
        @wraps(fn)
        def _recorded(self, arg):
            self._record_call(fn.__name__, arg, exclude_top_level)
            return fn(self, arg)
        return _recorded
    return _record_call

class Query():
    model_type = FeatureRecord

    def __init__(self):
        # The field key must equal exactly value, or re.search if a compiled regex
        self._value_equals = dict()

        # The field of type list named key must contain value
        self._list_contains = dict()

        # The field named key must equal one of the sub value in the list value
        self._value_equals_one_of = dict()

        self._calls = OrderedDict()
        self._top_level_excluded_calls = set()

    @property
    def value_equals(self):
        return self._value_equals

    @property
    def list_contains(self):
        return self._list_contains

    @property
    def value_equals_one_of(self):
        return self._value_equals_one_of

    def _record_call(self, fn_name, arg, exclude_top_level=False):
        self._calls[fn_name] = arg
        if exclude_top_level:
            self._top_level_excluded_calls.add(fn_name)

    def add_call(self, fn_name, arg):
        getattr(self, fn_name)(arg)

    @record_call(exclude_top_level=True)
    def name_regex_is(self, regex):
        self._value_equals[self.model_type.name.name_] = re.compile(regex)
        return self
    
    def type_is(self, cls):
        return self.type_is_str(cls._type)

    @record_call(exclude_top_level=True)
    def type_is_str(self, cls_str):
        self._value_equals['_type'] = cls_str
        return self

    def type_any_of(self, classes):
        return self.type_any_of_str([cls._type for cls in classes])
    
    @record_call(exclude_top_level=True)
    def type_any_of_str(self, classes_str):
        self._value_equals_one_of['_type'] = classes_str
        return self

    def tag_is(self, **tag_values):
        return self.tag_is_raw(tag_values)

    def tag_regex_is(self, **tag_regexes):
        return self.tag_is_raw({key: re.compile(value) for key, value in tag_regexes.items()})

    @record_call(exclude_top_level=False)
    def tag_is_raw(self, tag_values):
        base_name = self.model_type.test_id.tags.name_
        for key, value in tag_values.items():
            self._value_equals['{}.{}'.format(base_name, key)] = value
        return self

    @record_call(exclude_top_level=False)
    def test_uuid_is(self, test_uuid):
        self._value_equals[self.model_type.test_id.test_uuid.name_] = test_uuid
        return self
    
    @record_call(exclude_top_level=False)
    def test_uuid_any_of(self, test_uuids):
        self._value_equals_one_of[self.model_type.test_id.test_uuid.name_] = test_uuids
        return self
    
    @record_call(exclude_top_level=False)
    def testbench_name_is(self, testbench_name):
        self._value_equals[self.model_type.test_id.testbench_name.name_] = testbench_name
        return self
    
    def outcome_is(self, **outcome_attributes):
        return self.outcome_is_raw(outcome_attributes)

    @record_call(exclude_top_level=False)
    def outcome_is_raw(self, outcome_attributes):
        for field_name, value in outcome_attributes.items():
            field = getattr(self.model_type.outcome, field_name)
            self._value_equals[field.name_] = value
        return self
    
    def dut_match(self, id=None, version=None):
        return self.dut_match_raw({'id': id, 'version': version})

    @record_call(exclude_top_level=False)
    def dut_match_raw(self, id_and_version):
        _id = id_and_version.get('id', None)
        _version = id_and_version.get('version', None)
        if _id is not None:
            self._value_equals[self.model_type.test_id.dut.id.name_] = re.compile(_id)
        if _version is not None:
            self._value_equals[self.model_type.test_id.dut.version.name_] = re.compile(_version)
        return self

    def custom_match(self, match):
        self._value_equals.update(match)
        return self

    def __eq__(self, other_q):
        same_len = len(self._calls) == len(other_q._calls)
        if not same_len:
            return False

        for key, value in self._calls.items():
            if key not in other_q._calls or other_q._calls[key] != value:
                return False
        
        return True

    def __repr__(self):
        return '{}(eq={}, one-of={}, contains={})'.format(
            self.__class__.__name__,
            repr(self._value_equals),
            repr(self._value_equals_one_of),
            repr(self._list_contains)
        )

    KEY_SEPARATOR = '::'
    def as_dict(self):
        serializer = get_json_serializer()
        deep_dict = serializer.serialize(self._calls)
        flat_dict = flatten_dict(deep_dict)
        return {self.KEY_SEPARATOR.join(key) : value for key, value in flat_dict.items()}

    @classmethod
    def from_dict(cls, _flat_separated_calls):
        calls = cls.parse_query_dict(_flat_separated_calls)
        query = cls()
        for fn_name, arg in calls.items():
            query.add_call(fn_name, arg)
        return query

    @classmethod
    def parse_query_dict(cls, _flat_separated_calls):
        flat_dict = {tuple(key.split(cls.KEY_SEPARATOR)): value for key, value in _flat_separated_calls.items()}
        return deepen_dict(flat_dict)

    def copy(self):
        return self.__class__.from_dict(self.as_dict())

    def create_top_level_query(self):
        data = self.as_dict()
        for key in self._top_level_excluded_calls:
            del data[key]
        
        top_level_query = self.from_dict(data)
        # Filter for top level
        return top_level_query.type_is(TestRecordSummary).name_regex_is('')

def multi_query_serialize(**queries):
    """ Serialized as key_subkey = subvalue for key key, query in queries.
    """

    result = {}

    for key, query in queries.items():
        if '_' in key:
            raise ValueError('Query key {!r} cannot contain an underscore.'.format(key))
        if query:
            for subkey, subvalue in query.as_dict().items():
                result['{}_{}'.format(key, subkey)] = subvalue
    
    return result

def multi_query_deserialize(_dict):
    queries = {}

    for key, value in _dict.items():
        query_name, fn_name = split_key(key)
        update(queries, {
            query_name: Query.parse_query_dict({fn_name: value})
        })
    
    return {query_name: Query.from_dict(query_dict) for query_name, query_dict in queries.items()}

def split_key(key):
    split_key = key.split('_')
    return split_key[0], '_'.join(split_key[1:])