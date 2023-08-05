import enum

from django.utils.translation import gettext_lazy as _


class LoadEnum(enum.Enum):
    STATIC = _("Render normally")
    LAZY = _("Render empty and load after the page is loaded")
    RELOAD = _("Render normally and reload after the page is loaded")
