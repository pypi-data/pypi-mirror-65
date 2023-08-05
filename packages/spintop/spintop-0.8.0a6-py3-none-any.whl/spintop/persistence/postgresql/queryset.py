import re
from sqlalchemy import or_, and_

from spintop.models import TestRecordSummary
from spintop.utils import AnonymousGetRecursive

class PostgreSQLQuery(object):
    def __init__(self, query):
        self.orig_query = query
    
    def build_data_query(self, test_record_table):
        """Only support test_uuids for now"""
        test_uuids = []
        queries = []

        for key, value in self.orig_query.value_equals.items():
            # data is stored as test_record: 
            if key == TestRecordSummary.test_id.test_uuid.name_:
                test_uuids.append(value)
            else:
                field = self._get_test_record_field(test_record_table, 'test_record.' + key)
                if isinstance(value, re.Pattern):
                    queries.append(field.astext.op("~")(value.pattern))
                else:
                    queries.append(field.astext == str(value))
        
        for key, value in self.orig_query.list_contains.items():
            raise NotImplementedError()

        for key, list_of_values in self.orig_query.value_equals_one_of.items():
            if key == TestRecordSummary.test_id.test_uuid.name_:
                test_uuids += list_of_values
            else:
                field = self._get_test_record_field(test_record_table, 'test_record.' + key)
                queries.append(field.in_(list_of_values))
        
        if test_uuids:
            queries.append(test_record_table.test_uuid.in_(test_uuids))

        return queries

    def _get_test_record_field(self, test_record_table, field_name):
        field = AnonymousGetRecursive(test_record_table.data)
        return field.get_recursive(field_name)