import datetime
import decimal
import json
import uuid

from .importer import TypeReference


class CustomJSONDecoder(json.JSONDecoder):
    def raw_decode(self, s, idx=0):
        obj, end = super().raw_decode(s, idx)
        obj = self.decode_any(obj)
        return obj, end

    def decode_any(self, obj):
        if isinstance(obj, dict):
            return self.decode_dict(obj)
        if isinstance(obj, list):
            return self.decode_list(obj)
        return obj

    def decode_list(self, obj: list):
        return [self.decode_any(o) for o in obj]

    def decode_dict(self, obj: dict):
        if set(obj.keys()) == {"__type__", "__value__"}:
            type_, value = obj["__type__"], obj["__value__"]
            if type_ == "datetime":
                return datetime.datetime.fromisoformat(value)
            elif type_ == "date":
                return datetime.date.fromisoformat(value)
            elif type_ == "time":
                return datetime.time.fromisoformat(value)
            elif type_ == "timedelta":
                return datetime.timedelta(seconds=value)
            elif type_ == "decimal":
                return decimal.Decimal(value)
            elif type_ == "uuid":
                return uuid.UUID(value)
            elif type_ == "typereference":
                return TypeReference(value)
            elif type_ == "type":
                return TypeReference(value).type

        return {key: self.decode_any(value) for key, value in obj.items()}


class CustomJSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time, decimal types, and
    UUIDs.
    """

    @staticmethod
    def wrap(type_, value):
        return {"__type__": type_, "__value__": value}

    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            return self.wrap("datetime", o.isoformat())
        elif isinstance(o, datetime.date):
            return self.wrap("date", o.isoformat())
        elif isinstance(o, datetime.time):
            return self.wrap("time", o.isoformat())
        elif isinstance(o, datetime.timedelta):
            return self.wrap("timedelta", o.total_seconds())
        elif isinstance(o, decimal.Decimal):
            return self.wrap("decimal", str(o))
        elif isinstance(o, uuid.UUID):
            return self.wrap("uuid", str(o))
        elif isinstance(o, TypeReference):
            return self.wrap("typereference", o.str)
        elif isinstance(o, type):
            return self.wrap("type", TypeReference(o).str)
        else:
            return super().default(o)
