import logging

from django.db import models
from django.forms import widgets, fields

from cms.models.pluginmodel import CMSPlugin

from .fields import JSONField, TypeReferenceField
from .importer import TypeReference
from .enums import LoadEnum


logger = logging.getLogger(__name__)


class Form(CMSPlugin):
    name = models.CharField(max_length=255)
    form_type = TypeReferenceField(max_length=255, default=TypeReference("django.forms.forms.Form"))
    meta_parameters = JSONField(default=dict, blank=True)
    auto_render_fields = models.BooleanField(default=False)
    load = models.CharField(
        max_length=255, choices=[(e.name, e.value) for e in LoadEnum], default=LoadEnum.RELOAD.name,
    )

    _fields = None
    _form = None
    render_inner_only = False

    @property
    def fields(self):
        if self._fields is None:
            self._fields = list(self._get_form_fields(self))
        return self._fields

    @property
    def form(self):
        if self._form is None:
            self._form = self.build_form_cls()()
        return self._form

    @form.setter
    def form(self, value):
        self._form = value

    @property
    def is_lazy(self):
        return self.load == LoadEnum.LAZY.name

    @property
    def is_static(self):
        return self.load == LoadEnum.STATIC.name

    @classmethod
    def _get_form_fields(cls, plugin):
        for plugin in plugin.child_plugin_instances or ():
            if isinstance(plugin, FormField):
                yield plugin
            else:
                yield from cls._get_form_fields(plugin)

    def get_child_plugin_instances(self):  # rendering hook
        self.init_fields()
        return self.child_plugin_instances

    def build_form_cls(self):
        form_cls = self.form_type.type
        form_body = {field.name: field.build_field() for field in self.fields}
        form_body["Meta"] = type("Meta", (), self.meta_parameters)
        return type("DynamicForm", (form_cls,), form_body)

    def init_fields(self):
        for field in self.fields:
            field.form = self.form
            field.bound_field = self.form[field.name]

    def __str__(self):
        return self.name


class FormField(CMSPlugin):
    name = models.CharField(max_length=255)
    field_type = TypeReferenceField(max_length=255, default=TypeReference("django.forms.fields.Field"))
    field_parameters = JSONField(default=dict, blank=True)

    form = None
    bound_field = None

    def build_field(self):
        field_cls = self.field_type.type
        kwargs = self.field_parameters.copy()
        for plugin in self.child_plugin_instances or ():
            if isinstance(plugin, FormWidget):
                kwargs["widget"] = plugin.build_widget()
            elif isinstance(plugin, ChoiceOption):
                if issubclass(field_cls, fields.ChoiceField):
                    kwargs.setdefault("choices", []).append((plugin.value, plugin.display))
                else:
                    logger.warning(f"Choices added to not choice field ignored in field {self.pk}")
        return field_cls(**kwargs)

    def __str__(self):
        return self.name


class FormWidget(CMSPlugin):
    widget_type = TypeReferenceField(max_length=255, default=TypeReference("django.forms.widgets.Widget"))
    widget_parameters = JSONField(default=dict, blank=True)

    def build_widget(self):
        return self.widget_type.type(**self.widget_parameters)

    def __str__(self):
        return self.widget_type.str.split(".")[-1]


class ChoiceOption(CMSPlugin):
    value = models.CharField(max_length=255, blank=True, default="")
    display = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.value} : {self.display}"


class FormButton(CMSPlugin):
    input_type = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, default="")
    value = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return self.name

    def render_button(self):
        return widgets.Input({"type": self.input_type}).render(self.name, self.value)


class FormSubmission(models.Model):
    form_name = models.CharField(max_length=255)
    data = JSONField(default=dict, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.form_name


class FormSubmissionFile(models.Model):
    submission = models.ForeignKey(FormSubmission, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=255)
    file = models.FileField(upload_to="cms_forms/")

    def __str__(self):
        return self.field_name
