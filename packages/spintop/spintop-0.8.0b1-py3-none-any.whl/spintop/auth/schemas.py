from marshmallow import Schema, fields

class CredentialsSchema(Schema):
    username = fields.String(allow_none=True)
    access_token = fields.String()
    refresh_token = fields.String(allow_none=True)
    org_id = fields.String(allow_none=True)
    refresh_module = fields.String()
    
credentials_schema = CredentialsSchema()