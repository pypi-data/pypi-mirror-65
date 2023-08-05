from django.urls import path
from .views import BaseFormSubmissionView
from .models import Form


urlpatterns = [
    path("form/<int:form_pk>/", BaseFormSubmissionView.as_view(model=Form), name="cms_forms.form_submission",)
]
