from django.contrib import admin

from .models import Form, FormField, FormWidget, ChoiceOption, FormSubmission, FormSubmissionFile


@admin.register(Form)
class FromAdmin(admin.ModelAdmin):
    pass


@admin.register(FormField)
class FormFieldAdmin(admin.ModelAdmin):
    pass


@admin.register(FormWidget)
class FormWidgetAdmin(admin.ModelAdmin):
    pass


@admin.register(ChoiceOption)
class ChoiceOptionAdmin(admin.ModelAdmin):
    pass


class FormSubmissionFileInline(admin.TabularInline):
    model = FormSubmissionFile
    extra = 0


@admin.register(FormSubmission)
class FormSubmissionAdmin(admin.ModelAdmin):
    list_display = ["form_name", "created"]
    list_filter = ["form_name"]
    date_hierarchy = "created"
    readonly_fields = ["created"]
    inlines = [FormSubmissionFileInline]
