import functools

from django.http import HttpResponse, Http404
from django.http.response import HttpResponseBase
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.cache import never_cache

from cms.plugin_rendering import ContentRenderer
from cms.utils.plugins import get_plugins
from sekizai.context import SekizaiContext

from .forms import BaseForm


def get_plugin(request, model, form_pk):
    form_obj = get_object_or_404(model, pk=form_pk)
    for plugin in get_plugins(request, form_obj.placeholder, None):
        if form_pk == plugin.pk:
            return plugin
    raise Http404()


def render_plugin(request, plugin):
    context = SekizaiContext({"request": request, "inner_only": True})
    return ContentRenderer(request).render_plugin(plugin, context)


class BaseFormSubmissionView(View):
    model = None

    def get_plugin(self, form_pk):
        plugin = get_plugin(self.request, self.model, form_pk)
        _, plugin_pl = plugin.get_plugin_instance()
        plugin.render_inner_only = True
        return plugin

    def save(self, plugin, form):
        default = functools.partial(BaseForm.cms_save, form)
        return getattr(form, "cms_save", default)(self.request, plugin)

    @method_decorator(ensure_csrf_cookie)
    @method_decorator(never_cache)
    def get(self, request, form_pk):
        plugin = self.get_plugin(form_pk)
        return HttpResponse(render_plugin(request, plugin))

    def post(self, request, form_pk):
        plugin = self.get_plugin(form_pk)
        form = plugin.build_form_cls()(request.POST, request.FILES)
        plugin.form = form
        if form.is_valid():
            response = self.save(plugin, form)
            if isinstance(response, HttpResponseBase):
                return response
        return HttpResponse(render_plugin(request, plugin))
