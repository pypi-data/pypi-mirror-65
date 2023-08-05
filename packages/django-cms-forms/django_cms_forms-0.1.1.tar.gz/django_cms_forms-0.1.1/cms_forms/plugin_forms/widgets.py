import logging

from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from ..models import FormWidget
from ..importer import TypeReference
from ..fields import JSONFormField


class BaseWidgetForm(forms.ModelForm):
    class Meta:
        model = FormWidget
        fields = ()

    widget_type = None
    widget_parameters = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_widget_kwargs()

    def load_widget_kwargs(self):
        kwargs = self.instance.widget_parameters
        for param in self.widget_parameters:
            field = self.fields[param]
            field.initial = kwargs.get(param, field.initial)

    def get_widget_kwargs(self):
        return {param: self.cleaned_data[param] for param in self.widget_parameters}

    def update_instance(self):
        self.instance.widget_parameters = self.get_widget_kwargs()
        self.instance.widget_type = self.widget_type

    def clean(self):
        res = super().clean()
        try:
            self.update_instance()
            self.instance.build_widget()
        except Exception as e:
            logging.exception("Form widget creation failed")
            raise forms.ValidationError(_("Form widget creation failed: %(error)s"), params={"error": e})
        return res


class WidgetForm(BaseWidgetForm):
    widget_type = TypeReference(widgets.Widget)
    widget_parameters = BaseWidgetForm.widget_parameters + ["attrs"]
    attrs_parameters = []

    attrs = JSONFormField(required=False, empty_value=None)

    def load_widget_kwargs(self):
        parameters = self.instance.widget_parameters or {}
        attrs = parameters.get("attrs", None) or {}
        for param in self.attrs_parameters:
            field = self.fields[param]
            field.initial = attrs.pop(param, field.initial)

        return super().load_widget_kwargs()

    def get_widget_kwargs(self):
        kwargs = super().get_widget_kwargs()
        attrs = {
            param: self.cleaned_data[param] for param in self.attrs_parameters if self.cleaned_data[param] is not None
        }
        extra_attrs = kwargs.pop("attrs", None) or {}
        attrs.update(extra_attrs)
        kwargs["attrs"] = attrs or None
        return kwargs


class InputForm(WidgetForm):
    widget_type = TypeReference(widgets.Input)
    attrs_parameters = WidgetForm.attrs_parameters + ["type"]

    type = forms.CharField(max_length=255, required=False, empty_value=None)


class TextInputForm(InputForm):
    widget_type = TypeReference(widgets.TextInput)


class NumberInputForm(InputForm):
    widget_type = TypeReference(widgets.NumberInput)


class EmailInputForm(InputForm):
    widget_type = TypeReference(widgets.EmailInput)


class URLInputForm(InputForm):
    widget_type = TypeReference(widgets.URLInput)


class PasswordInputForm(InputForm):
    widget_type = TypeReference(widgets.PasswordInput)
    widget_parameters = InputForm.widget_parameters + ["render_value"]

    render_value = forms.BooleanField(required=False, initial=False)


class HiddenInputForm(InputForm):
    widget_type = TypeReference(widgets.HiddenInput)


class MultipleHiddenInputForm(HiddenInputForm):
    widget_type = TypeReference(widgets.MultipleHiddenInput)


class FileInputForm(InputForm):
    widget_type = TypeReference(widgets.FileInput)


class ClearableFileInputForm(FileInputForm):
    widget_type = TypeReference(widgets.ClearableFileInput)


class TextareaForm(WidgetForm):
    widget_type = TypeReference(widgets.Textarea)
    attrs_parameters = WidgetForm.attrs_parameters + ["cols", "rows"]

    cols = forms.IntegerField(required=False, min_value=0)
    rows = forms.IntegerField(required=False, min_value=0)


class DateTimeBaseInputForm(InputForm):
    widget_type = TypeReference(widgets.DateTimeBaseInput)
    widget_parameters = InputForm.widget_parameters + ["format"]

    format = forms.CharField(required=False, empty_value=None)


class DateInputForm(DateTimeBaseInputForm):
    widget_type = TypeReference(widgets.DateInput)


class DateTimeInputForm(DateTimeBaseInputForm):
    widget_type = TypeReference(widgets.DateTimeInput)


class TimeInputForm(DateTimeBaseInputForm):
    widget_type = TypeReference(widgets.TimeInput)


class CheckboxInputForm(InputForm):
    widget_type = TypeReference(widgets.CheckboxInput)
    # TODO: check_test


class ChoiceWidgetForm(WidgetForm):
    widget_type = TypeReference(widgets.ChoiceWidget)
    # TODO: choices


class SelectForm(ChoiceWidgetForm):
    widget_type = TypeReference(widgets.Select)


class NullBooleanSelectForm(SelectForm):
    widget_type = TypeReference(widgets.NullBooleanSelect)
    widget_parameters = [p for p in SelectForm.widget_parameters if p != "choices"]

    choices = None


class SelectMultipleForm(SelectForm):
    widget_type = TypeReference(widgets.SelectMultiple)


class CheckboxSelectMultipleForm(ChoiceWidgetForm):
    widget_type = TypeReference(widgets.CheckboxSelectMultiple)


class MultiWidgetForm(WidgetForm):
    widget_type = TypeReference(widgets.MultiWidget)
    # TODO: widgets


class SplitDateTimeWidgetForm(MultiWidgetForm):
    widget_type = TypeReference(widgets.SplitDateTimeWidget)
    widget_parameters = MultiWidgetForm.widget_parameters + ["date_format", "time_format", "date_attrs", "time_attrs"]

    date_format = forms.CharField(required=False)
    time_format = forms.CharField(required=False)
    date_attrs = JSONFormField(required=False, empty_value=None)
    time_attrs = JSONFormField(required=False, empty_value=None)


class SplitHiddenDateTimeWidgetForm(SplitDateTimeWidgetForm):
    widget_type = TypeReference(widgets.SplitHiddenDateTimeWidget)


class SelectDateWidgetForm(WidgetForm):
    widget_type = TypeReference(widgets.SelectDateWidget)
    widget_parameters = WidgetForm.attrs_parameters + ["years", "months", "empty_label"]

    years = JSONFormField(required=False, empty_value=None)
    months = JSONFormField(required=False, empty_value=None)
    empty_label = forms.CharField(required=False)
