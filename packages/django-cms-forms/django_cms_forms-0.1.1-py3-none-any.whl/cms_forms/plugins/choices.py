from cms.plugin_base import CMSPluginBase
from django.utils.translation import gettext_lazy as _

from ..models import ChoiceOption
from ..plugin_forms import choices
from .. import config


class ChoiceOptionPlugin(CMSPluginBase):
    module = _("Form Choices")
    model = ChoiceOption
    name = _("Choice")
    form = choices.ChoiceOptionForm
    render_plugin = False
    require_parent = True
    parent_classes = config.CHOICE_FIELD_PLUGIN_NAMES
