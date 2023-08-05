from cms.plugin_pool import plugin_pool

from .importer import TypeReference
from . import config


if config.FORMS_REGISTER_PLUGINS:
    for src in [
        config.FORM_PLUGINS,
        config.FIELD_PLUGINS,
        config.WIDGET_PLUGINS,
        config.CHOICE_OPTION_PLUGINS,
        config.BUTTON_PLUGINS,
    ]:
        for plugin_str in src:
            plugin = TypeReference(plugin_str).type
            plugin_pool.register_plugin(plugin)
