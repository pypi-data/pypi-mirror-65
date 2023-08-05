import typing
from django.conf import settings

from . import config_defaults


def name(s: str) -> str:
    return s.split(".")[-1]


def configure(key: str):
    return getattr(settings, f"CMS_{key}", getattr(config_defaults, key))


FORMS_REGISTER_PLUGINS: bool = configure("FORMS_REGISTER_PLUGINS")

FORM_PLUGINS: typing.List[str] = configure("FORM_PLUGINS")
FIELD_PLUGINS: typing.List[str] = configure("FIELD_PLUGINS")
WIDGET_PLUGINS: typing.List[str] = configure("WIDGET_PLUGINS")
CHOICE_OPTION_PLUGINS: typing.List[str] = configure("CHOICE_OPTION_PLUGINS")
CHOICE_FIELD_PLUGINS: typing.List[str] = configure("CHOICE_FIELD_PLUGINS")
BUTTON_PLUGINS: typing.List[str] = configure("BUTTON_PLUGINS")

FORM_PLUGIN_NAMES: typing.List[str] = [name(p) for p in FORM_PLUGINS]
FIELD_PLUGIN_NAMES: typing.List[str] = [name(p) for p in FIELD_PLUGINS]
WIDGET_PLUGIN_NAMES: typing.List[str] = [name(p) for p in WIDGET_PLUGINS]
CHOICE_OPTION_PLUGIN_NAMES: typing.List[str] = [name(p) for p in CHOICE_OPTION_PLUGINS]
CHOICE_FIELD_PLUGIN_NAMES: typing.List[str] = [name(p) for p in CHOICE_FIELD_PLUGINS]
BUTTON_PLUGIN_NAMES: typing.List[str] = [name(p) for p in BUTTON_PLUGINS]
