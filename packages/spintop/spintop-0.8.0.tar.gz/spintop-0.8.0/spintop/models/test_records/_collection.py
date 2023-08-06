from itertools import chain

from collections import OrderedDict, defaultdict
from collections.abc import Mapping
from typing import NamedTuple, List

from spintop.utils import GetRecursive, GetRecursiveMixin, dict_ops

from ..base import (
    is_serialized_type_of, 
    type_dict_of
)
from ..view import DataClassPrimitiveView, ComplexPrimitiveView

from ._base import (
    BaseDataClass, 
    TestIDRecord, 
    TestRecordSummary, 
    FeatureRecord, 
    DefaultPrimitiveView, 
    compute_stats,
    serialized_get_test_uuid
)


SUPPORT_MISSING_TOP_LEVEL_RECORD = False

def normalize_features_len(dict_array):
    new_dict = {}
    max_column_key_len = max([len(key) for key in dict_array])
    for key, value in dict_array.items():
        if len(key) < max_column_key_len:
            key = key + ('',)*(max_column_key_len - len(key))
        new_dict[key] = value
    return new_dict
    
            
class SpintopTestRecordCollection(object):
    def __init__(self, flat_records=None):
        self.records = list(flat_records) if flat_records else []
    
    @property
    def collector(self):
        return self.add_record

    @property
    def test_uuids(self):
        return [record.test_uuid for record in self.records]

    def add_record(self, record):
        self.records.append(record)
        
    def apply(self, *fns):
        for record in self.iter_records():
            for fn in fns:
                fn(record)
                
    def iter_records(self):
        for record in self.records:
            yield record
                
    def count_unique(self, key=lambda record: record.test_id.test_uuid):
        occurances = set()
        self.apply(lambda record: occurances.add(key(record)))
        return len(occurances)
            
    def are_records_unique(self):
        test_uuids = self.test_uuids
        return len(test_uuids) == len(set(test_uuids))

    def sort(self, key=lambda record: record.test_id.start_datetime):
        self.records.sort(key=key)
        
    def avg_feature_count(self):
        feature_counts = [len(record.features) for record in self.iter_records()]
        return sum(feature_counts)/len(feature_counts)
    
    def __eq__(self, other):
        return self.records == other.records

class SpintopTestRecord(GetRecursiveMixin):
    def __init__(self, test_record, features=None):
        self._data = None
        self._features = None
        
        if test_record is None:
            raise ValueError('None test_record is not supported.')

        self.data = test_record # The top-level data
        self.features = tuple(features) if features else tuple()
    
    @property
    def features(self):
        return self._features if self._features else tuple()
    
    @features.setter
    def features(self, features):

        self._broadcast_test_id(features)
        self._features = tuple(sorted(features, key=lambda feature: feature.index))
        
    @property
    def all_features(self):
        return (self.data,) + self.features

    def compute_stats(self):
        if not self.data.feature_count:
            compute_stats(self.all_features)

    @property
    def data(self):
        return self._data

    @property
    def test_record(self):
        return self.data
    
    @data.setter
    def data(self, value):
        self._data = value
        self._broadcast_test_id(self.features)
        
    @property
    def test_id(self):
        return self.data.test_id

    @property
    def test_uuid(self):
        return self.test_id.test_uuid
    
    def __hash__(self):
        return hash(self.test_uuid)

    def __eq__(self, other):
        return self.data == other.data and self.features == other.features
    
    def __repr__(self):
        return '{}(test_record={!r}, features=[...]*{})'.format(self.__class__.__name__, self.data, len(self.features))

    def remove_duplicate_features(self):
        feature_names = set()
        features = []
        for feature in self.features:
            if feature.name in feature_names:
                continue
            else:
                features.append(feature)
                feature_names.add(feature.name)
        
        self.features = features
    
    def _broadcast_test_id(self, features):
        """Uses the top level test_id and sets it for all features, ensuring
        that all features have the same TestIDRecord reference."""
        for feature in features:
            feature.test_id = self.data.test_id
    
    def reindex(self):
        for index, feature in enumerate(self.features):
            feature.index = index

    def normalize_outcomes(self):
        parents = tuple()
        last_feature = None
        for feature in self.all_features:
            while feature.depth > len(parents):
                if last_feature.name not in feature.ancestors:
                    raise Exception('Unable to normalize outcomes: feature order does not match ancestors. {!r} should be in ancestors: {!r}'.format(
                        last_feature.name,
                        feature.ancestors
                    )) 
                parents = parents + (last_feature,)

            if feature.depth < len(parents):
                parents = parents[:feature.depth]

            outcome = feature.outcome

            for parent in reversed(parents):
                outcome.impose_upon(parent.outcome)
                outcome = parent.outcome

            last_feature = feature

            
    def fill_missing_from_source(self, fill_source, on_fill=None):
        max_current_feature_index = max(self.features, key=lambda f: f.index)
        new_features_len = len(fill_source)
        
        assert new_features_len >= max_current_feature_index.index, "Fill source must be same length or bigger than this test_record max index."
        
        new_features = [None]*new_features_len
        
        if on_fill is None:
            on_fill = lambda obj: obj.copy()
            
        def fill_range(start, end):
            for i in range(start, end):
                new_features[i] = on_fill(fill_source[i])
        
        current_index = 0
        for feature in sorted(self.features, key=lambda f: f.index):
            fill_range(current_index, feature.index)
            new_features[feature.index] = feature # Keep this feature
            current_index = feature.index + 1
        
        fill_range(current_index, new_features_len) # Fill end
        
        self.features = new_features
                
    def find_feature(self, condition, start_index=0):
        try:
            return next(feat for feat in self.all_features[start_index:] if condition(feat))
        except StopIteration:
            raise ValueError('No feature matched condition.')
    
    def add_tag(self, key, value=True):
        self.test_id.add_tag(key, value=value)
        
    def remove_tag(self, key):
        self.test_id.remove_tag(key)

    def as_dict(self):
        return dict(
            test_record=self._data,
            features=list(self._features)
        )

    @classmethod
    def from_dict(cls, _dict):
        return cls(**_dict)

class SpintopTestRecordView(object):
    feature_prefix = ('features', lambda feat: feat._type, lambda feat: feat.complete_name)
    data_prefix = () 
    default_view = DefaultPrimitiveView()
    
    def __init__(self, feature_mapping=None, include_test_id=True):
        self.include_test_id = include_test_id

        if feature_mapping:
            self.feature_view = DataClassPrimitiveView(feature_mapping)
        else:
            self.feature_view = self.default_view

    def apply(self, record, flatten_dict=True):
        data = OrderedDict()
        
        if self.include_test_id:
            test_id_data = self.apply_default_test_id(record, flatten_dict=flatten_dict)
            dict_ops.update(data, test_id_data)
        
        for feature in record.features:
            feature_data = self.feature_view.apply(feature, flatten_dict=flatten_dict)
            dict_ops.update(data, feature_data)
        
        data = dict_ops.replace_defaults(data)

        return data
    
    def apply_default_feature(self, feature, key_prefix=None, **apply_kwargs):
        if key_prefix is None: key_prefix = self.feature_prefix
        return self.feature_view.apply(feature, key_prefix=key_prefix, **apply_kwargs)
    
    def apply_default_test_id(self, record, key_prefix=None, **apply_kwargs):
        if key_prefix is None: key_prefix = self.data_prefix
        data = self.default_view.apply(record.data, key_prefix=key_prefix, **apply_kwargs)
        return data

class SpintopFlatTestRecordBuilder(NamedTuple):
    test_record: TestRecordSummary
    features: List[FeatureRecord]
    
    def build(self):
        record = SpintopTestRecord(test_record=self.test_record, features=sorted(self.features, key=lambda feature: feature.index))
        record.compute_stats()
        return record

class SpintopSerializedFlatTestRecord(GetRecursiveMixin):

    def __init__(self, test_record=None, features=[]):
        self.test_record = test_record
        self.features = features

    @property
    def data(self):
        return GetRecursive(self.test_record)

    @property
    def test_id(self):
        return GetRecursive(self.test_record['test_id'])

    @property
    def test_uuid(self):
        return self.test_id['test_uuid']

    @property
    def all_features(self):
        return (self.test_record,) + tuple(self.features)

    def as_dict(self):
        return dict(
            test_record=self.test_record,
            features=self.features
        )

    def deserialize(self, serializer):
        builder = SpintopFlatTestRecordBuilder(
            test_record=serializer.deserialize(BaseDataClass, self.test_record), 
            features=tuple(serializer.deserialize(BaseDataClass, feat) for feat in self.features)
        )
        return builder.build()

    def __repr__(self):
        return '{}(test_record={!r}, features=[...]*{})'.format(self.__class__.__name__, self.test_record, len(self.features))

    def __eq__(self, other):
        return self.as_dict() == other.as_dict()

class SpintopSerializedTestRecordCollection(object):

    def __init__(self, records=[]):
        self.records = [
            SpintopSerializedFlatTestRecord(**record) if isinstance(record, Mapping) else record 
            for record in records
        ]

    @classmethod
    def from_features(cls, features):
        return cls(records=serialized_features_to_record_list(features))

    def deserialize(self, serializer):
        return (record.deserialize(serializer) for record in self.records)

def serialized_features_to_record_list(features):
    test_uuid_record_map = OrderedDict()
    
    for feature in features:
        found_test_record = None
        found_feature = None

        if is_serialized_type_of(feature, TestRecordSummary):
            found_test_record = feature
        else:
            found_feature = feature
        
        test_uuid = serialized_get_test_uuid(feature)

        record = test_uuid_record_map.get(test_uuid, None)
        if record is None:
            record = SpintopSerializedFlatTestRecord(test_record=None, features=[])
        
        if found_test_record:
            if record.test_record is not None:
                raise ValueError('Two features match as a top level record for the same record: {!r} and {!r}'.format(record.test_record, found_test_record))
            record.test_record = found_test_record
        else:
            record.features.append(found_feature)

        test_uuid_record_map[test_uuid] = record
    
    records = list(test_uuid_record_map.values())

    for record in records:
        if record.test_record is None:
            # Find a valid test_id from features.
            if SUPPORT_MISSING_TOP_LEVEL_RECORD:
                test_id = None
                if record.features:
                    test_id = record.features[0]['test_id']
                else:
                    raise ValueError('Empty Test Record.')
                record.test_record = TestRecordSummary.null(test_id=test_id, original=False).as_dict()
            else:
                raise RuntimeError('Missing top level record from SpintopTestRecord {!r}'.format(record))

    return records

        
        
    