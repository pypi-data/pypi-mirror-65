from marshmallow import Schema, fields, pprint
from uuid import getnode

from ..auth.schemas import CredentialsSchema

class SpintopAPIProfile(Schema):
    credentials_key = fields.String(allow_none=True)
    spintop_api_url = fields.String(allow_none=True)
    name = fields.String(allow_none=True)
    
class SpintopMachineConfig(Schema):
    """
    hardware_uuid: xxxxxxxx
    credentials:
        1234:
            access_token:
            refresh_token:
            username:
    
    """
    default_profile = fields.String(default='default')
    hardware_uuid = fields.String(default=getnode)
    profiles = fields.Dict(keys=fields.Str(), values=fields.Nested(SpintopAPIProfile()))
    credentials = fields.Dict(keys=fields.Str(), values=fields.Nested(CredentialsSchema()))
    