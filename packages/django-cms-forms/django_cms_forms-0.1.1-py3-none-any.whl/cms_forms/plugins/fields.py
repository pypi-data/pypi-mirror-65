from cms.plugin_base import CMSPluginBase
from django.utils.translation import gettext_lazy as _

from ..models import FormField
from ..plugin_forms import fields
from .. import config


def extra_fieldset(form=None, exclude=None, name=None, _fields=None):
    if exclude is None:
        exclude = fields.FieldForm.field_parameters
    if _fields is None:
        _fields = [f for f in form.field_parameters if f not in exclude]
    if _fields:
        return [(name, {"fields": _fields})]
    return []


def build_fieldsets(base, form, split=1, **kwargs):
    before, after = base.fieldsets[:split], base.fieldsets[split:]
    kwargs.setdefault("exclude", []).extend([f for fs in base.fieldsets for f in fs[1]["fields"]])
    return before + extra_fieldset(form, **kwargs) + after


class FormFieldPlugin(CMSPluginBase):
    module = _("Form Fields")
    model = FormField
    name = _("Field")
    render_template = "cms_forms/formfieldplugin.html"
    field_template = "cms_forms/field.html"
    form = fields.FieldForm
    fieldsets = extra_fieldset(name=_("Name"), _fields=["name"]) + extra_fieldset(
        fields.FieldForm, exclude=[], name=_("Base field parameters")
    )
    allow_children = True
    child_classes = config.WIDGET_PLUGIN_NAMES

    def render(self, *args, **kwargs):
        context = super().render(*args, **kwargs)
        context["plugin"] = self
        return context


class CharFieldPlugin(FormFieldPlugin):
    name = _("Char field")
    form = fields.CharFieldForm
    fieldsets = build_fieldsets(FormFieldPlugin, fields.CharFieldForm, name=_("Char parameters"))


class IntegerFieldPlugin(FormFieldPlugin):
    name = _("Integer field")
    form = fields.IntegerFieldForm
    fieldsets = build_fieldsets(FormFieldPlugin, fields.IntegerFieldForm, name=_("Integer parameters"))


class FloatFieldPlugin(IntegerFieldPlugin):
    name = _("Float field")
    form = fields.FloatFieldForm
    fieldsets = build_fieldsets(IntegerFieldPlugin, fields.FloatFieldForm, name=_("Float parameters"))


class DecimalFieldPlugin(IntegerFieldPlugin):
    name = _("Decimal field")
    form = fields.DecimalFieldForm
    fieldsets = build_fieldsets(IntegerFieldPlugin, fields.DecimalFieldForm, name=_("Decimal parameters"))


class BaseTemporalFieldPlugin(FormFieldPlugin):
    form = fields.BaseTemporalFieldForm


class DateFieldPlugin(BaseTemporalFieldPlugin):
    name = _("Date field")
    form = fields.DateFieldForm
    fieldsets = build_fieldsets(BaseTemporalFieldPlugin, fields.DateFieldForm, name=_("Date parameters"))


class TimeFieldPlugin(BaseTemporalFieldPlugin):
    name = _("Time field")
    form = fields.TimeFieldForm
    fieldsets = build_fieldsets(BaseTemporalFieldPlugin, fields.TimeFieldForm, name=_("Time parameters"))


class DateTimeFieldPlugin(BaseTemporalFieldPlugin):
    name = _("DateTime field")
    form = fields.DateTimeFieldForm
    fieldsets = build_fieldsets(BaseTemporalFieldPlugin, fields.DateTimeFieldForm, name=_("DateTime parameters"))


class DurationFieldPlugin(FormFieldPlugin):
    name = _("Duration field")
    form = fields.DurationFieldForm
    fieldsets = build_fieldsets(FormFieldPlugin, fields.DurationFieldForm, name=_("Duration parameters"))


class RegexFieldPlugin(CharFieldPlugin):
    name = _("Regex field")
    form = fields.RegexFieldForm
    fieldsets = build_fieldsets(CharFieldPlugin, fields.RegexFieldForm, name=_("Regex parameters"))


class EmailFieldPlugin(CharFieldPlugin):
    name = _("Email field")
    form = fields.EmailFieldForm
    fieldsets = (
        extra_fieldset(name=_("Name"), _fields=["name"])
        + extra_fieldset(fields.EmailFieldForm, name=_("Email parameters"))
        + extra_fieldset(fields.CharFieldForm, exclude=["strip"], name=_("Base field parameters"))
    )


class FileFieldPlugin(FormFieldPlugin):
    name = _("File field")
    form = fields.FileFieldForm
    fieldsets = build_fieldsets(FormFieldPlugin, fields.FileFieldForm, name=_("File parameters"))


class ImageFieldPlugin(FileFieldPlugin):
    name = _("Image field")
    form = fields.ImageFieldForm
    fieldsets = build_fieldsets(FileFieldPlugin, fields.ImageFieldForm, name=_("Image parameters"))


class URLFieldPlugin(CharFieldPlugin):
    name = _("URL field")
    form = fields.URLFieldForm
    fieldsets = (
        extra_fieldset(name=_("Name"), _fields=["name"])
        + extra_fieldset(fields.URLFieldForm, name=_("URL parameters"))
        + extra_fieldset(fields.CharFieldForm, exclude=["strip"], name=_("Base field parameters"))
    )


class BooleanFieldPlugin(FormFieldPlugin):
    name = _("Boolean field")
    form = fields.BooleanFieldForm
    fieldsets = build_fieldsets(FormFieldPlugin, fields.BooleanFieldForm, name=_("Boolean parameters"))


class NullBooleanFieldPlugin(BooleanFieldPlugin):
    name = _("NullBoolean field")
    form = fields.NullBooleanFieldForm
    fieldsets = build_fieldsets(BooleanFieldPlugin, fields.NullBooleanFieldForm, name=_("NullBoolean parameters"))


class ChoiceFieldPlugin(FormFieldPlugin):
    name = _("Choice field")
    form = fields.ChoiceFieldForm
    fieldsets = build_fieldsets(FormFieldPlugin, fields.ChoiceFieldForm, name=_("Choice parameters"))
    child_classes = FormFieldPlugin.child_classes + config.CHOICE_OPTION_PLUGIN_NAMES


class TypedChoiceFieldPlugin(ChoiceFieldPlugin):
    name = _("TypedChoice field")
    form = fields.TypedChoiceFieldForm
    fieldsets = build_fieldsets(ChoiceFieldPlugin, fields.TypedChoiceFieldForm, name=_("TypedChoice parameters"))


class MultipleChoiceFieldPlugin(ChoiceFieldPlugin):
    name = _("MultipleChoice field")
    form = fields.MultipleChoiceFieldForm
    fieldsets = build_fieldsets(ChoiceFieldPlugin, fields.MultipleChoiceFieldForm, name=_("MultipleChoice parameters"))


class TypedMultipleChoiceFieldPlugin(ChoiceFieldPlugin):
    name = _("TypedMultipleChoice field")
    form = fields.TypedMultipleChoiceFieldForm
    fieldsets = build_fieldsets(
        ChoiceFieldPlugin, fields.TypedMultipleChoiceFieldForm, name=_("TypedMultipleChoice parameters")
    )


class ComboFieldPlugin(FormFieldPlugin):
    name = _("Combo field")
    form = fields.ComboFieldForm
    fieldsets = build_fieldsets(FormFieldPlugin, fields.ComboFieldForm, name=_("Combo parameters"))


class MultiValueFieldPlugin(FormFieldPlugin):
    name = _("MultiValue field")
    form = fields.MultiValueFieldForm
    fieldsets = build_fieldsets(FormFieldPlugin, fields.MultiValueFieldForm, name=_("MultiValue parameters"))


class FilePathFieldPlugin(ChoiceFieldPlugin):
    name = _("FilePath field")
    form = fields.FilePathFieldForm
    fieldsets = build_fieldsets(ChoiceFieldPlugin, fields.FilePathFieldForm, name=_("FilePath parameters"))


class SplitDateTimeFieldPlugin(MultiValueFieldPlugin):
    name = _("SplitDateTime field")
    form = fields.SplitDateTimeFieldForm
    fieldsets = build_fieldsets(
        MultiValueFieldPlugin, fields.SplitDateTimeFieldForm, name=_("SplitDateTime parameters")
    )


class GenericIPAddressFieldPlugin(CharFieldPlugin):
    name = _("GenericIPAddress field")
    form = fields.GenericIPAddressFieldForm
    fieldsets = build_fieldsets(
        CharFieldPlugin, fields.GenericIPAddressFieldForm, name=_("GenericIPAddress parameters")
    )


class SlugFieldPlugin(CharFieldPlugin):
    name = _("Slug field")
    form = fields.SlugFieldForm
    fieldsets = build_fieldsets(CharFieldPlugin, fields.SlugFieldForm, name=_("Slug parameters"))


class UUIDFieldPlugin(CharFieldPlugin):
    name = _("UUID field")
    form = fields.UUIDFieldForm
    fieldsets = build_fieldsets(CharFieldPlugin, fields.UUIDFieldForm, name=_("UUID parameters"))
