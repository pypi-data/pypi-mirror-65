from cms.plugin_base import CMSPluginBase
from django.utils.translation import gettext_lazy as _

from ..models import FormButton
from ..plugin_forms import buttons


class BaseButtonPlugin(CMSPluginBase):
    module = _("Form buttons")
    model = FormButton
    form = buttons.BaseButtonForm
    name = _("Button")
    render_template = "cms_forms/formbutton.html"


class ButtonPlugin(BaseButtonPlugin):
    form = buttons.ButtonForm


class SubmitButtonPlugin(BaseButtonPlugin):
    form = buttons.SubmitButtonForm
    name = _("Submit button")


class ResetButtonPlugin(BaseButtonPlugin):
    form = buttons.ResetButtonForm
    name = _("Reset button")
