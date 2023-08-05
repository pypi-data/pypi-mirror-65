import dateutil.parser
from functools import lru_cache
from datetime import datetime
from time import mktime
from copy import deepcopy

from dataclasses_serialization.serializer_base import dict_to_dataclass, dict_serialization, list_deserialization, noop_deserialization, noop_serialization

from .base import BaseDataClass
from .test_records import SpintopTestRecord, SpintopSerializedFlatTestRecord

from spintop.utils import local_tz, isnan

def get_serializer():
    return get_bson_serializer()

@lru_cache(maxsize=128)
def get_bson_serializer():
    """Make or return the singleton SpintopBSONSerializer"""
    from dataclasses_serialization.bson import BSONSerializer
    serializer = deepcopy(BSONSerializer)
    _make_serializer(serializer)
    return serializer

@lru_cache(maxsize=128)
def get_json_serializer(datetime_serializer=lambda datetime_obj: datetime_obj.timestamp()):
    from dataclasses_serialization.json import JSONSerializer
    serializer = deepcopy(JSONSerializer)
    _make_serializer(serializer, datetime_serializer=datetime_serializer)
    return serializer

def _make_serializer(serializer, datetime_serializer=lambda datetime_obj: datetime_obj):
    orig_deserialize = serializer.deserialize
    def wrapped_deserialize(cls, obj):
        """ Always support any obj that is None. Default implementation
        will raise an error if obj is None and the type of a dataclass
        field is anything but Any or None
        """
        if obj is None:
            return None
        else:
            return orig_deserialize(cls, obj)
    
    serializer.deserialize = wrapped_deserialize
    
    # The base serializer has an entry of type: (str, int, ...): noop_serializer
    # Because the key contains many types, if we want to overwrite one of them, we
    # get the risk that the default one gets picked. Therefore, we split the key
    # in individual functions before adding our customs one which may overwrite these
    # ones.
    _split_key_of_op(serializer.deserialization_functions, noop_deserialization)
    _split_key_of_op(serializer.serialization_functions, noop_serialization)

    @serializer.register_serializer(float)
    def serialize_nan(f_value):
        if isnan(f_value):
            return None
        else:
            return f_value

    @serializer.register_serializer(datetime)
    def serialize_datetime(obj):
        # obj = obj.astimezone(local_tz())
        return datetime_serializer(obj)

    @serializer.register_deserializer(datetime)
    def deserialize_datetime(cls, obj):
        datetime_obj = None
        if isinstance(obj, str):
            datetime_obj = dateutil.parser.parse(obj)
        elif isinstance(obj, datetime):
            datetime_obj = obj 
        else:
            datetime_obj = datetime.fromtimestamp(obj)
        return datetime_obj
        # return datetime_obj.astimezone(local_tz())

    @serializer.register_serializer(BaseDataClass)
    def serialize(obj):
        """Custom serializer for BaseDataClass that extracts the static
        attribute '_type' into the serialized dict for future deserialization."""
        data = dict_serialization(dict(obj.__dict__), key_serialization_func=serializer.serialize, value_serialization_func=serializer.serialize)
        data.update({'_type': obj._type})
        return data

    @serializer.register_deserializer(BaseDataClass)
    def deserialize(cls, obj):
        """ Custom deserializer that infers the BaseDataClass subclass based
        on the _type attribute. 
        """
        # Strips the _type field and returns the sub cls, if found. Else returns the cls
        # as passed in parameter
        cls, obj = BaseDataClass.cls_data_from_dict(cls, obj)
        return dict_to_dataclass(cls, obj, deserialization_func=serializer.deserialize)

    
    @serializer.register_serializer((SpintopTestRecord, SpintopSerializedFlatTestRecord))
    def serialize_spintop_test_record(obj):
        return serializer.serialize(obj.as_dict())

    @serializer.register_deserializer(SpintopTestRecord)
    def deserialize_spintop_test_record(cls, obj):
        result = {}
        if isinstance(obj, SpintopSerializedFlatTestRecord):
            result = obj.as_dict()
        else:
            if 'test_record' in obj:
                result['test_record'] = serializer.deserialize(BaseDataClass, obj['test_record'])
            
            if 'features' in obj:
                result['features'] = [serializer.deserialize(BaseDataClass, feat) for feat in obj['features']]

        return cls.from_dict(result)
    
    return serializer

def _split_key_of_op(op_map, op_fn):
    key_is = None

    for key, fn in op_map.items():
        if fn is op_fn:
            key_is = key
            break
    
    if key_is is None:
        raise ValueError(f'Did not find {op_fn} in map.')
    elif not isinstance(key_is, tuple):
        return
    else:
        del op_map[key_is]
    
        for key in  key_is:
            op_map[key] = op_fn

