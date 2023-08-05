import json

from django.core.exceptions import ValidationError
from django.db import models
from django import forms

from .json import CustomJSONEncoder, CustomJSONDecoder
from .importer import TypeReference


class JSONField(models.TextField):
    def from_db_value(self, value, *args, **kwargs):
        return self.to_python(value)

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, str):
            try:
                value = json.loads(value, cls=CustomJSONDecoder)
            except json.JSONDecodeError:
                raise ValidationError("Unable to load JSON")
        return value

    def get_prep_value(self, value):
        if not isinstance(value, str):
            value = json.dumps(value, cls=CustomJSONEncoder)
        return value

    def value_to_string(self, obj):
        return self.get_prep_value(obj)

    def formfield(self, **kwargs):
        kwargs.setdefault("form_class", JSONFormField)
        return super().formfield(**kwargs)


class JSONFormField(forms.CharField):
    widget = forms.Textarea

    def prepare_value(self, value):
        if not isinstance(value, str):
            value = json.dumps(value, cls=CustomJSONEncoder)
        return value

    def to_python(self, value):
        value = super().to_python(value)
        if value in self.empty_values:
            return None
        if isinstance(value, str):
            try:
                value = json.loads(value, cls=CustomJSONDecoder)
            except json.JSONDecodeError:
                raise ValidationError("Unable to load JSON")
        return value


class TypeReferenceField(models.CharField):
    def from_db_value(self, value, *args, **kwargs):
        return self.to_python(value)

    def to_python(self, value):
        if not value:
            return None
        try:
            return TypeReference(value)
        except ImportError:
            raise ValidationError("Unable to find type")

    def get_prep_value(self, value):
        if value is None:
            return value
        return TypeReference(value).str

    def value_to_string(self, obj):
        return self.get_prep_value(obj)

    def formfield(self, **kwargs):
        kwargs.setdefault("form_class", TypeReferenceFormField)
        return super().formfield(**kwargs)


class TypeReferenceFormField(forms.CharField):
    def prepare_value(self, value):
        if not value:
            return None
        return value

    def to_python(self, value):
        value = super().to_python(value)
        if not value:
            return None
        try:
            return TypeReference(value)
        except ImportError:
            raise ValidationError("Unable to find type")
