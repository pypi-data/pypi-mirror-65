from . import MeasureFeatureRecord

def value_of_feature_named(name):
    name_field = MeasureFeatureRecord.name.name_
    value_fields = [
        MeasureFeatureRecord.value_f.name_,
        MeasureFeatureRecord.value_s.name_,
    ]
    def _accessor(feat):
        if feat.get_recursive(name_field) != name:
            raise AttributeError('Wrong feature')
        else:
            for value_field in value_fields:
                value = feat.get_recursive(value_field)
                if value is not None:
                    break
            return value
    return _accessor