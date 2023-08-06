from dataclasses import dataclass, fields, field, Field

class MetaBaseDataClass(type):
    def __getattr__(cls, key):
        """ Allows fields to be accessed from class. I.e. 
        
        @dataclass()
        class MyDataClass(BaseDataClass):
            my_field: str
            
        MyDataClass.my_field.name == 'my_field'
        """
        try:
            return cls.get_field(key)
        except AttributeError:
            return super().__getattribute__(key)
    
    def get_field(cls, key, parent_fields=()):
        # no cache here has the cls might be being build.
        for field in fields(cls):
            if field.name == key:
                return MetaField(cls, field, parents=parent_fields)
        else:
            raise AttributeError(key)


class MetaField(Field):
    def __init__(self, cls, field, parents=()):
        self.__type = cls
        self.__parents = parents
        self.__field = field
    
    @property
    def name_(self):
        return '.'.join(self.name_tuple_)

    @property
    def type_(self):
        return self.__field.type

    @property
    def container_type_(self):
        if self.__parents:
            return self.__parents[0].__type
        else:
            return self.__type

    @property
    def name_tuple_(self):
        return tuple(parent.__field.name for parent in (self.__parents + (self,))) 

    def value_of_serialized(self, serialized_obj):
        for field_name in self.name_tuple_:
            serialized_obj = serialized_obj[field_name]
        
        return serialized_obj

    def is_container_of_cls(self, cls):
        return cls is self.container_type_ or issubclass(cls, self.container_type_)

    def __getattr__(self, key):
        try:
            return self.__field.type.get_field(key, parent_fields=self.__parents + (self,))
        except AttributeError:
            return getattr(self.__field, key)

    def __hash__(self):
        return hash(self.__field)
    
    def __eq__(self, other):
        return self.__field == other.__field

    
# def make_operation(field, op_on_value):
#     return lambda real_obj: op_on_value(getattr(real_obj, field.name))
