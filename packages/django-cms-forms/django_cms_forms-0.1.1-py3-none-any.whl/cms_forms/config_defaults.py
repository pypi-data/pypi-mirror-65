FORMS_REGISTER_PLUGINS = True

FORM_PLUGINS = [
    "cms_forms.plugins.forms.FormPlugin",
    "cms_forms.plugins.forms.ModelFormPlugin",
    "cms_forms.plugins.forms.SavingFormPlugin",
]

FIELD_PLUGINS = [
    "cms_forms.plugins.fields.CharFieldPlugin",
    "cms_forms.plugins.fields.IntegerFieldPlugin",
    "cms_forms.plugins.fields.FloatFieldPlugin",
    "cms_forms.plugins.fields.DecimalFieldPlugin",
    "cms_forms.plugins.fields.DateFieldPlugin",
    "cms_forms.plugins.fields.TimeFieldPlugin",
    "cms_forms.plugins.fields.DateTimeFieldPlugin",
    "cms_forms.plugins.fields.DurationFieldPlugin",
    "cms_forms.plugins.fields.RegexFieldPlugin",
    "cms_forms.plugins.fields.EmailFieldPlugin",
    "cms_forms.plugins.fields.FileFieldPlugin",
    "cms_forms.plugins.fields.ImageFieldPlugin",
    "cms_forms.plugins.fields.URLFieldPlugin",
    "cms_forms.plugins.fields.BooleanFieldPlugin",
    "cms_forms.plugins.fields.NullBooleanFieldPlugin",
    "cms_forms.plugins.fields.ChoiceFieldPlugin",
    "cms_forms.plugins.fields.TypedChoiceFieldPlugin",
    "cms_forms.plugins.fields.MultipleChoiceFieldPlugin",
    "cms_forms.plugins.fields.TypedMultipleChoiceFieldPlugin",
    "cms_forms.plugins.fields.FilePathFieldPlugin",
    "cms_forms.plugins.fields.SplitDateTimeFieldPlugin",
    "cms_forms.plugins.fields.GenericIPAddressFieldPlugin",
    "cms_forms.plugins.fields.SlugFieldPlugin",
    "cms_forms.plugins.fields.UUIDFieldPlugin",
]

WIDGET_PLUGINS = [
    "cms_forms.plugins.widgets.TextInputPlugin",
    "cms_forms.plugins.widgets.NumberInputPlugin",
    "cms_forms.plugins.widgets.EmailInputPlugin",
    "cms_forms.plugins.widgets.URLInputPlugin",
    "cms_forms.plugins.widgets.PasswordInputPlugin",
    "cms_forms.plugins.widgets.HiddenInputPlugin",
    "cms_forms.plugins.widgets.MultipleHiddenInputPlugin",
    "cms_forms.plugins.widgets.FileInputPlugin",
    "cms_forms.plugins.widgets.ClearableFileInputPlugin",
    "cms_forms.plugins.widgets.TextareaPlugin",
    "cms_forms.plugins.widgets.DateInputPlugin",
    "cms_forms.plugins.widgets.DateTimeInputPlugin",
    "cms_forms.plugins.widgets.TimeInputPlugin",
    "cms_forms.plugins.widgets.CheckboxInputPlugin",
    "cms_forms.plugins.widgets.ChoiceWidgetPlugin",
    "cms_forms.plugins.widgets.SelectPlugin",
    "cms_forms.plugins.widgets.NullBooleanSelectPlugin",
    "cms_forms.plugins.widgets.SelectMultiplePlugin",
    "cms_forms.plugins.widgets.CheckboxSelectMultiplePlugin",
    "cms_forms.plugins.widgets.SplitDateTimeWidgetPlugin",
    "cms_forms.plugins.widgets.SplitHiddenDateTimeWidgetPlugin",
    "cms_forms.plugins.widgets.SelectDateWidgetPlugin",
]

CHOICE_OPTION_PLUGINS = [
    "cms_forms.plugins.choices.ChoiceOptionPlugin",
]

CHOICE_FIELD_PLUGINS = [
    "cms_forms.plugins.fields.ChoiceFieldPlugin",
    "cms_forms.plugins.fields.TypedChoiceFieldPlugin",
    "cms_forms.plugins.fields.MultipleChoiceFieldPlugin",
    "cms_forms.plugins.fields.TypedMultipleChoiceFieldPlugin",
]

BUTTON_PLUGINS = [
    "cms_forms.plugins.buttons.ButtonPlugin",
    "cms_forms.plugins.buttons.SubmitButtonPlugin",
    "cms_forms.plugins.buttons.ResetButtonPlugin",
]
