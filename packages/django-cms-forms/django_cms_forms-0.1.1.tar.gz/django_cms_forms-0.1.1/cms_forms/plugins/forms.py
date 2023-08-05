from cms.plugin_base import CMSPluginBase
from django.utils.translation import gettext_lazy as _

from ..models import Form
from ..plugin_forms import forms


class BaseFormPlugin(CMSPluginBase):
    module = _("Forms")
    model = Form
    form = forms.BaseFormForm
    name = _("Form")
    render_template = "cms_forms/formplugin.html"
    auto_render_field_template = "cms_forms/field.html"
    allow_children = True

    def render(self, *args, **kwargs):
        context = super().render(*args, **kwargs)
        context["plugin"] = self
        return context


class FormPlugin(BaseFormPlugin):
    form = forms.FormForm
    name = _("Form")


class ModelFormPlugin(FormPlugin):
    form = forms.ModelFormForm
    name = _("Model form")


class SavingFormPlugin(FormPlugin):
    form = forms.SavingFormForm
    name = _("Saving form")
