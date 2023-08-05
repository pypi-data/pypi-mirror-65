import logging

from django import forms
from django.forms import fields
from django.utils.translation import gettext_lazy as _

from ..models import FormField
from ..importer import TypeReference
from ..fields import JSONFormField


class BaseFieldForm(forms.ModelForm):
    class Meta:
        model = FormField
        fields = ("name",)

    field_type = None
    field_parameters = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_field_kwargs()

    def load_field_kwargs(self):
        kwargs = self.instance.field_parameters
        for param in self.field_parameters:
            field = self.fields[param]
            field.initial = kwargs.get(param, field.initial)

    def get_field_kwargs(self):
        return {param: self.cleaned_data[param] for param in self.field_parameters}

    def update_instance(self):
        self.instance.field_parameters = self.get_field_kwargs()
        self.instance.field_type = self.field_type

    def clean(self):
        res = super().clean()
        try:
            self.update_instance()
            self.instance.build_field()
        except Exception as e:
            logging.exception("Form field creation failed")
            raise forms.ValidationError(_("Form field creation failed: %(error)s"), params={"error": e})
        return res


class FieldForm(BaseFieldForm):
    field_type = TypeReference(fields.Field)
    field_parameters = BaseFieldForm.field_parameters + [
        "required",
        "label",
        "initial",
        "help_text",
        "show_hidden_initial",
        "localize",
        "disabled",
        "label_suffix",
    ]

    required = forms.BooleanField(required=False, initial=True)
    label = forms.CharField(required=False, empty_value=None)
    initial = forms.Field(required=False)
    help_text = forms.CharField(required=False, empty_value=None)
    error_messages = None  # TODO?
    show_hidden_initial = forms.BooleanField(required=False, initial=False)
    validators = ()  # TODO?
    localize = forms.BooleanField(required=False, initial=False)
    disabled = forms.BooleanField(required=False, initial=False)
    label_suffix = forms.CharField(required=False, empty_value=None)


class CharFieldForm(FieldForm):
    field_type = TypeReference(fields.CharField)
    field_parameters = FieldForm.field_parameters + ["max_length", "min_length", "strip", "empty_value"]

    initial = forms.CharField(required=False)
    max_length = forms.IntegerField(required=False, min_value=0)
    min_length = forms.IntegerField(required=False, min_value=0)
    strip = forms.BooleanField(required=False, initial=True)
    empty_value = forms.CharField(required=False, empty_value="")


class IntegerFieldForm(FieldForm):
    field_type = TypeReference(fields.IntegerField)
    field_parameters = FieldForm.field_parameters + ["max_value", "min_value"]

    initial = forms.IntegerField(required=False)
    max_value = forms.IntegerField(required=False)
    min_value = forms.IntegerField(required=False)


class FloatFieldForm(IntegerFieldForm):
    field_type = TypeReference(fields.FloatField)

    initial = forms.FloatField(required=False)
    max_value = forms.FloatField(required=False)
    min_value = forms.FloatField(required=False)


class DecimalFieldForm(IntegerFieldForm):
    field_type = TypeReference(fields.DecimalField)
    field_parameters = IntegerFieldForm.field_parameters + ["max_digits", "decimal_places"]

    initial = forms.DecimalField(required=False)
    max_value = forms.DecimalField(required=False)
    min_value = forms.DecimalField(required=False)
    max_digits = forms.IntegerField(required=False)
    decimal_places = forms.IntegerField(required=False)


class BaseTemporalFieldForm(FieldForm):
    field_type = TypeReference(fields.BaseTemporalField)

    input_formats = None  # TODO
    initial = fields.BaseTemporalField(required=False)


class DateFieldForm(BaseTemporalFieldForm):
    field_type = TypeReference(fields.DateField)

    initial = forms.DateField(required=False)


class TimeFieldForm(BaseTemporalFieldForm):
    field_type = TypeReference(fields.TimeField)

    initial = forms.TimeField(required=False)


class DateTimeFieldForm(BaseTemporalFieldForm):
    field_type = TypeReference(fields.DateTimeField)

    initial = forms.DateTimeField(required=False)


class DurationFieldForm(FieldForm):
    field_type = TypeReference(fields.DurationField)

    initial = forms.DurationField(required=False)


class RegexFieldForm(CharFieldForm):
    field_type = TypeReference(fields.RegexField)
    field_parameters = CharFieldForm.field_parameters + ["regex"]

    initial = forms.CharField(required=False)
    strip = forms.BooleanField(required=False, initial=False)
    regex = forms.CharField()


class EmailFieldForm(CharFieldForm):
    field_type = TypeReference(fields.EmailField)
    field_parameters = [p for p in CharFieldForm.field_parameters if p != "strip"]

    initial = forms.EmailField(required=False)
    strip = None


class FileFieldForm(FieldForm):
    field_type = TypeReference(fields.FileField)
    field_parameters = FieldForm.field_parameters + ["max_length", "allow_empty_file"]

    # TODO: initial?

    max_length = forms.IntegerField(required=False, min_value=0)
    allow_empty_file = forms.BooleanField(required=False, initial=False)


class ImageFieldForm(FileFieldForm):
    field_type = TypeReference(fields.ImageField)


class URLFieldForm(CharFieldForm):
    field_type = TypeReference(fields.URLField)
    field_parameters = [p for p in CharFieldForm.field_parameters if p != "strip"]

    initial = forms.URLField(required=False)
    strip = None


class BooleanFieldForm(FieldForm):
    field_type = TypeReference(fields.BooleanField)

    initial = forms.NullBooleanField(required=False)


class NullBooleanFieldForm(BooleanFieldForm):
    field_type = TypeReference(fields.NullBooleanField)

    initial = forms.NullBooleanField(required=False)


class ChoiceFieldForm(FieldForm):
    field_type = TypeReference(fields.ChoiceField)

    initial = forms.CharField(required=False)
    # choices  # TODO


class TypedChoiceFieldForm(ChoiceFieldForm):
    field_type = TypeReference(fields.TypedChoiceField)
    field_parameters = ChoiceFieldForm.field_parameters + ["empty_value"]

    initial = forms.CharField(required=False)
    # TODO: coerce
    empty_value = JSONFormField(required=False, empty_value="")


class MultipleChoiceFieldForm(ChoiceFieldForm):
    field_type = TypeReference(fields.MultipleChoiceField)

    initial = JSONFormField(required=False, empty_value=None)


class TypedMultipleChoiceFieldForm(ChoiceFieldForm):
    field_type = TypeReference(fields.TypedMultipleChoiceField)
    # TODO: coerce
    initial = JSONFormField(required=False, empty_value=None)


class ComboFieldForm(FieldForm):
    field_type = TypeReference(fields.ComboField)
    # TODO: fields, initial


class MultiValueFieldForm(FieldForm):
    field_type = TypeReference(fields.MultiValueField)
    field_parameters = FieldForm.field_parameters + ["require_all_fields"]
    # TODO: fields, initial

    require_all_fields = forms.BooleanField(required=False, initial=False)


class FilePathFieldForm(ChoiceFieldForm):
    field_type = TypeReference(fields.FilePathField)
    field_parameters = ChoiceFieldForm.field_parameters + ["path", "match", "recursive", "allow_files", "allow_folders"]

    initial = forms.CharField(required=False)
    path = forms.CharField()
    match = forms.CharField(required=False, empty_value=None)
    recursive = forms.BooleanField(required=False, initial=False)
    allow_files = forms.BooleanField(required=False, initial=True)
    allow_folders = forms.BooleanField(required=False, initial=False)


class SplitDateTimeFieldForm(MultiValueFieldForm):
    field_type = TypeReference(fields.SplitDateTimeField)
    # TODO: input_date_formats, input_time_formats


class GenericIPAddressFieldForm(CharFieldForm):
    field_type = TypeReference(fields.GenericIPAddressField)
    field_parameters = CharFieldForm.field_parameters + ["protocol", "unpack_ipv4"]

    initial = forms.GenericIPAddressField(required=False)
    protocol = forms.ChoiceField(choices=(("ipv4", "IPv4"), ("ipv6", "IPv6"), ("both", _("Both"))), initial="both")
    unpack_ipv4 = forms.BooleanField(required=False, initial=False)


class SlugFieldForm(CharFieldForm):
    field_type = TypeReference(fields.SlugField)
    field_parameters = CharFieldForm.field_parameters + ["allow_unicode"]

    initial = forms.SlugField(required=False)
    allow_unicode = forms.BooleanField(required=False, initial=False)


class UUIDFieldForm(CharFieldForm):
    field_type = TypeReference(fields.UUIDField)

    initial = forms.UUIDField(required=False)
