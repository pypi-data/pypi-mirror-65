import dateutil.parser
from typing import Union
from functools import lru_cache
from datetime import datetime
from time import mktime
from copy import deepcopy, copy

from dataclasses_serialization.serializer_base import (
    dataclass,
    Serializer, 
    dict_to_dataclass, 
    dict_serialization, 
    noop_serialization,
    dict_deserialization,
    list_deserialization, 
    union_deserialization,
    noop_deserialization, 
)

from .base import BaseDataClass
from .test_records import SpintopTestRecord, SpintopSerializedFlatTestRecord

from spintop.utils import local_tz, isnan


def get_serializer():
    return get_bson_serializer()

@lru_cache(maxsize=128)
def get_bson_serializer():
    """Make or return the singleton SpintopBSONSerializer"""
    from dataclasses_serialization.bson import BSONSerializer
    serializer = _SpintopSerializer(BSONSerializer)
    return serializer

@lru_cache(maxsize=128)
def get_json_serializer(datetime_serializer=lambda datetime_obj: datetime_obj.timestamp()):
    from dataclasses_serialization.json import JSONSerializer
    serializer = _SpintopSerializer(JSONSerializer, datetime_serializer=datetime_serializer)
    return serializer

def _copy_serializer(serializer):
    return 

class _SpintopSerializer(Serializer):
    def __init__(self, source_ser, datetime_serializer=noop_serialization):
        super().__init__(
            serialization_functions=copy(source_ser.serialization_functions),
            deserialization_functions=copy(source_ser.deserialization_functions)
        )
        self._make_serializer(datetime_serializer=datetime_serializer)

    def __post_init__(self):
        for ser_map in (self.serialization_functions, self.deserialization_functions):
            try:
                del ser_map[dataclass]
            except KeyError:
                pass
        self.deserialization_functions.setdefault(Union, union_deserialization(deserialization_func=self.deserialize))

    def deserialize(self, cls, obj):
        """ Always support any obj that is None. Default implementation
        will raise an error if obj is None and the type of a dataclass
        field is anything but Any or None
        """
        if obj is None:
            return None
        else:
            return super().deserialize(cls, obj)

    def _make_serializer(self, datetime_serializer=lambda datetime_obj: datetime_obj):
        
        # The base serializer has an entry of type: (str, int, ...): noop_serializer
        # Because the key contains many types, if we want to overwrite one of them, we
        # get the risk that the default one gets picked. Therefore, we split the key
        # in individual functions before adding our customs one which may overwrite these
        # ones.
        _split_key_of_op(self.deserialization_functions, noop_deserialization)
        _split_key_of_op(self.serialization_functions, noop_serialization)

        self.register(
            dict,
            serialization_func = lambda dct: dict_serialization(dct, key_serialization_func=self.serialize, value_serialization_func=self.serialize),
            deserialization_func = lambda cls, dct: dict_deserialization(cls, dct, key_deserialization_func=self.deserialize, value_deserialization_func=self.deserialize)
        )

        self.register(
            list,
            serialization_func = lambda lst: list(map(self.serialize, lst)),
            deserialization_func = lambda cls, lst: list_deserialization(cls, lst, deserialization_func=self.deserialize)
        )

        @self.register_serializer(float)
        def serialize_nan(f_value):
            if isnan(f_value):
                return None
            else:
                return f_value

        @self.register_serializer(datetime)
        def serialize_datetime(obj):
            # obj = obj.astimezone(local_tz())
            return datetime_serializer(obj)

        @self.register_deserializer(datetime)
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

        @self.register_serializer(BaseDataClass)
        def serialize(obj):
            """Custom serializer for BaseDataClass that extracts the static
            attribute '_type' into the serialized dict for future deserialization."""
            data = dict_serialization(dict(obj.__dict__), key_serialization_func=self.serialize, value_serialization_func=self.serialize)
            data.update({'_type': obj._type})
            return data

        @self.register_deserializer(BaseDataClass)
        def deserialize(cls, obj):
            """ Custom deserializer that infers the BaseDataClass subclass based
            on the _type attribute. 
            """
            # Strips the _type field and returns the sub cls, if found. Else returns the cls
            # as passed in parameter
            cls, obj = BaseDataClass.cls_data_from_dict(cls, obj)
            return dict_to_dataclass(cls, obj, deserialization_func=self.deserialize)

        
        @self.register_serializer((SpintopTestRecord, SpintopSerializedFlatTestRecord))
        def serialize_spintop_test_record(obj):
            return self.serialize(obj.as_dict())

        @self.register_deserializer(SpintopTestRecord)
        def deserialize_spintop_test_record(cls, obj):
            result = {}
            if isinstance(obj, SpintopSerializedFlatTestRecord):
                result = obj.as_dict()
            else:
                if 'test_record' in obj:
                    result['test_record'] = self.deserialize(BaseDataClass, obj['test_record'])
                
                if 'features' in obj:
                    result['features'] = [self.deserialize(BaseDataClass, feat) for feat in obj['features']]

            return cls.from_dict(result)
        

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

