from django import forms

from ..models import FormButton


class BaseButtonForm(forms.ModelForm):
    class Meta:
        model = FormButton
        fields = ["name", "value"]

    input_type = None

    def clean(self):
        res = super().clean()
        self.instance.input_type = self.input_type
        return res


class ButtonForm(BaseButtonForm):
    input_type = "button"


class SubmitButtonForm(BaseButtonForm):
    input_type = "submit"


class ResetButtonForm(BaseButtonForm):
    input_type = "reset"
