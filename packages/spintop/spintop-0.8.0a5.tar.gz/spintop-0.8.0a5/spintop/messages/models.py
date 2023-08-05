from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union

from spintop.models import SpintopTestRecord, SpintopSerializedFlatTestRecord

@dataclass
class SpintopEnvMessage():
    env: Optional[Dict[str, Optional[Any]]]

    def create_message_env(self, local_env):
        """Create a copy of the local env with the attributes contained in this message"""
        env = self.env
        if env is None:
            env = {}
        return local_env.copy(**env)

    @classmethod
    def from_message(cls, other_env_message, **kwargs):
        obj = cls(env=other_env_message.env, **kwargs)
        return obj

@dataclass
class TestRecordMessage(SpintopEnvMessage):
    test_record: Union[SpintopTestRecord, SpintopSerializedFlatTestRecord]

@dataclass
class TestsUpdateMessage(SpintopEnvMessage):
    updated_test_uuids: List[str]
    deleted_test_uuids: List[str]
    affected_duts: List[str]
    update_all: bool = False
    delete_all: bool = False

    @classmethod
    def create(self, **kwargs):
        defaults = dict(
            updated_test_uuids = [],
            deleted_test_uuids = [],
            affected_duts = [],
            update_all = False,
            delete_all = False,
            env = None
        )
        defaults.update(kwargs)
        return TestsUpdateMessage(**defaults)

@dataclass
class TestsUpdateQueryMessage(SpintopEnvMessage):
    query_dict: Dict[str, Any]
