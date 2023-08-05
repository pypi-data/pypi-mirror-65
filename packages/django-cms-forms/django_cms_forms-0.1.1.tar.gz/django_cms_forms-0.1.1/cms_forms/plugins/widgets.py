from cms.plugin_base import CMSPluginBase
from django.utils.translation import gettext_lazy as _

from ..models import FormWidget
from ..plugin_forms import widgets
from .. import config


class WidgetPlugin(CMSPluginBase):
    module = _("Form Widgets")
    model = FormWidget
    name = _("Widget")
    form = widgets.WidgetForm
    render_plugin = False
    require_parent = True
    parent_classes = config.FIELD_PLUGIN_NAMES

    def render(self, *args, **kwargs):
        context = super().render(*args, **kwargs)
        context["plugin"] = self
        return context


class InputPlugin(WidgetPlugin):
    name = _("Input")
    form = widgets.InputForm


class TextInputPlugin(InputPlugin):
    name = _("Text input")
    form = widgets.TextInputForm


class NumberInputPlugin(InputPlugin):
    name = _("Number input")
    form = widgets.NumberInputForm


class EmailInputPlugin(InputPlugin):
    name = _("Email input")
    form = widgets.EmailInputForm


class URLInputPlugin(InputPlugin):
    name = _("URL input")
    form = widgets.URLInputForm


class PasswordInputPlugin(InputPlugin):
    name = _("Password input")
    form = widgets.PasswordInputForm


class HiddenInputPlugin(InputPlugin):
    name = _("Hidden input")
    form = widgets.HiddenInputForm


class MultipleHiddenInputPlugin(HiddenInputPlugin):
    name = _("Multiple hidden input")
    form = widgets.MultipleHiddenInputForm


class FileInputPlugin(InputPlugin):
    name = _("File input")
    form = widgets.FileInputForm


class ClearableFileInputPlugin(FileInputPlugin):
    name = _("Clearable file input")
    form = widgets.ClearableFileInputForm


class TextareaPlugin(WidgetPlugin):
    name = _("Textarea")
    form = widgets.TextareaForm


class DateTimeBaseInput(InputPlugin):
    name = _("Datetime base input")
    form = widgets.DateTimeBaseInputForm


class DateInputPlugin(DateTimeBaseInput):
    name = _("Date input")
    form = widgets.DateInputForm


class DateTimeInputPlugin(DateTimeBaseInput):
    name = _("DateTime input")
    form = widgets.DateTimeInputForm


class TimeInputPlugin(DateTimeBaseInput):
    name = _("Time input")
    form = widgets.TimeInputForm


class CheckboxInputPlugin(InputPlugin):
    name = _("Checkbox input")
    form = widgets.CheckboxInputForm


class ChoiceWidgetPlugin(WidgetPlugin):
    name = _("Choice widget")
    form = widgets.ChoiceWidgetForm


class SelectPlugin(ChoiceWidgetPlugin):
    name = _("Select")
    form = widgets.SelectForm


class NullBooleanSelectPlugin(SelectPlugin):
    name = _("Null boolean select")
    form = widgets.NullBooleanSelectForm


class SelectMultiplePlugin(SelectPlugin):
    name = _("Select multiple")
    form = widgets.SelectMultipleForm


class CheckboxSelectMultiplePlugin(ChoiceWidgetPlugin):
    name = _("Checkbox select multiple")
    form = widgets.CheckboxSelectMultipleForm


class MultiWidgetPlugin(WidgetPlugin):
    name = _("Multi widget")
    form = widgets.MultiWidgetForm


class SplitDateTimeWidgetPlugin(MultiWidgetPlugin):
    name = _("Split datetime widget")
    form = widgets.SplitDateTimeWidgetForm


class SplitHiddenDateTimeWidgetPlugin(SplitDateTimeWidgetPlugin):
    name = _("Split hidden datetime widget")
    form = widgets.SplitHiddenDateTimeWidgetForm


class SelectDateWidgetPlugin(WidgetPlugin):
    name = _("Select date widget")
    form = widgets.SelectDateWidgetForm
