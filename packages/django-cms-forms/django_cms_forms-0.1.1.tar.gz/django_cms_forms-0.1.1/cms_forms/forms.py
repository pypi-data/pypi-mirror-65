from django import forms
from django.core.files.base import File
from django.http import HttpResponse, HttpResponseRedirect

from .models import FormSubmission, FormSubmissionFile


class BaseForm(forms.Form):
    """Interface for custom forms"""

    def cms_save(self, request, plugin):
        return getattr(self, "save", lambda: None)()


class SavingForm(BaseForm):
    @staticmethod
    def save_data(data, form_name):
        files = {}
        for key, value in data.items():
            if isinstance(value, File):
                files[key] = value
        for key in files.keys():
            data.pop(key)
        submission = FormSubmission.objects.create(form_name=form_name, data=data,)
        for key, value in files.items():
            FormSubmissionFile.objects.create(
                submission=submission, field_name=key, file=value,
            )
        return submission

    def cms_save(self, request, plugin):
        self.save_data(self.cleaned_data.copy(), plugin.name)
        success_url = plugin.meta_parameters.get("success_url", None)
        if success_url:
            return HttpResponseRedirect(success_url)
        success_content = plugin.meta_parameters.get("success_content", None)
        if success_content:
            return HttpResponse(success_content)
