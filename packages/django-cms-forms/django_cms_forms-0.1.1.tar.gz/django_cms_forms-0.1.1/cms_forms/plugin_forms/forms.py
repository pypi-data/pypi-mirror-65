import logging

from django import forms
from django.apps import apps
from django.utils.translation import gettext_lazy as _

from ..importer import TypeReference
from ..models import Form
from ..forms import SavingForm


class BaseFormForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ("name", "auto_render_fields", "load")

    form_type = None

    def update_instance(self):
        self.instance.form_type = self.form_type

    def clean(self):
        res = super().clean()
        try:
            self.update_instance()
            self.instance.build_form_cls()()
        except Exception as e:
            logging.exception("Form creation failed")
            raise forms.ValidationError(_("Form creation failed: %(error)s"), params={"error": e})
        return res


class FormForm(BaseFormForm):
    form_type = TypeReference(forms.Form)


class BaseModelFormForm(FormForm):
    meta_parameters = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_meta_kwargs(self.instance.meta_parameters.copy())

    def load_meta_kwargs(self, kwargs):
        for param in self.meta_parameters:
            field = self.fields[param]
            field.initial = kwargs.get(param, field.initial)

    def get_meta_kwargs(self):
        return {param: self.cleaned_data[param] for param in self.meta_parameters if param in self.cleaned_data}

    def update_instance(self):
        self.instance.meta_parameters = self.get_meta_kwargs()
        return super().update_instance()


class ModelFormForm(BaseModelFormForm):
    form_type = TypeReference(forms.ModelForm)
    meta_parameters = ["model", "fields", "exclude"]

    model = forms.ChoiceField()
    fields = forms.CharField(required=False, empty_value=None, initial="__all__")
    exclude = forms.CharField(required=False, empty_value=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["model"].choices = [
            (TypeReference(model).str, TypeReference(model).str) for model in apps.get_models()
        ]

    @staticmethod
    def split_fields(fields):
        if fields == "__all__" or fields is None:
            return fields
        return fields.split(",")

    def get_meta_kwargs(self):
        kwargs = super().get_meta_kwargs()
        kwargs["model"] = TypeReference(self.cleaned_data["model"]).type
        fields = kwargs["fields"]
        kwargs["fields"] = self.split_fields(fields)
        exclude = kwargs["exclude"]
        kwargs["exclude"] = self.split_fields(exclude)
        return kwargs

    def load_meta_kwargs(self, kwargs):
        model = kwargs.pop("model", None)
        kwargs["model"] = TypeReference(model).str if model else None
        fields = kwargs.pop("fields", "__all__")
        kwargs["fields"] = ",".join(fields) if isinstance(fields, list) else fields
        exclude = kwargs.pop("exclude", None)
        kwargs["exclude"] = ",".join(exclude) if isinstance(exclude, list) else exclude
        return super().load_meta_kwargs(kwargs)


class SavingFormForm(BaseModelFormForm):
    form_type = TypeReference(SavingForm)
    meta_parameters = ["success_url", "success_content"]

    success_url = forms.CharField(required=False)
    success_content = forms.CharField(required=False, widget=forms.Textarea)
