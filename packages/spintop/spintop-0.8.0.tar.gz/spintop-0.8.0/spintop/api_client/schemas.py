from marshmallow import Schema, fields

class ManyTestsSchema(Schema):
    tests = fields.List(fields.Dict())
    
class TestsCountSchema(Schema):
    count = fields.Int()

tests_schema = ManyTestsSchema()
test_count_schema = TestsCountSchema()

