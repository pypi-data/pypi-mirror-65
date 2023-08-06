from functools import lru_cache, wraps

import marshmallow_dataclass

@lru_cache()
def get_schema(message_model_cls):
    Schema = marshmallow_dataclass.class_schema(message_model_cls)
    return Schema()