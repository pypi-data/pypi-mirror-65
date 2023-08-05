from django import forms

from ..models import ChoiceOption


class ChoiceOptionForm(forms.ModelForm):
    class Meta:
        model = ChoiceOption
        fields = ("value", "display")
