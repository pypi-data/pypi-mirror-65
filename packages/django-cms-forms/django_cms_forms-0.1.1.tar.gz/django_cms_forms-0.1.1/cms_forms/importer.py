import weakref

from django.utils.module_loading import import_string


class TypeReference:
    def __init__(self, obj):
        if isinstance(obj, TypeReference):
            self.str = obj.str
            self.type = obj.type
        elif isinstance(obj, str):
            self.str = obj
            self.type = Importer.from_string(obj)
        else:
            self.str = Importer.to_string(obj)
            self.type = obj

    def __repr__(self):
        return f"{self.__class__.__qualname__}({self.str!r})"

    def __eq__(self, other):
        if not other:
            return False
        try:
            other_tr = TypeReference(other)
        except ImportError:
            return False
        return self.str == other_tr.str

    def __str__(self):
        return self.str

    def __len__(self):
        return len(self.str)

    def deconstruct(self):
        return f"{self.__class__.__module__}.{self.__class__.__qualname__}", [self.str], {}


class Importer:
    registry = weakref.WeakValueDictionary()

    @classmethod
    def from_string(cls, s):
        if isinstance(s, TypeReference):
            return s.type
        if s not in cls.registry:
            cls.registry[s] = import_string(s)
        return cls.registry[s]

    @classmethod
    def to_string(cls, c):
        if isinstance(c, TypeReference):
            return c.str
        return f"{c.__module__}.{c.__qualname__}"
