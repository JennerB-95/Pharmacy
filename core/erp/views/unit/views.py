from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import UnitForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Unit


class UnitListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Unit
    template_name = 'unit/list.html'
    permission_required = 'view_unit'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                position = 1
                for i in Unit.objects.all():
                    item = i.toJSON()
                    item['position'] = position
                    data.append(item)
                    position += 1
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Unidades de Medida'
        context['create_url'] = reverse_lazy('erp:unit_create')
        context['list_url'] = reverse_lazy('erp:unit_list')
        context['entity'] = 'Unidades de Medida'
        return context


class UnitCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Unit
    form_class = UnitForm
    template_name = 'unit/create.html'
    success_url = reverse_lazy('erp:unit_list')
    permission_required = 'add_unit'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Unidad de Medida'
        context['entity'] = 'Unidad de Medida'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class UnitUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Unit
    form_class = UnitForm
    template_name = 'unit/create.html'
    success_url = reverse_lazy('erp:unit_list')
    permission_required = 'change_unit'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Unidad de Medida'
        context['entity'] = 'Unidades de Medida'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class UnitDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Unit
    template_name = 'unit/delete.html'
    success_url = reverse_lazy('erp:unit_list')
    permission_required = 'delete_unit'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Unidad'
        context['entity'] = 'Unidades'
        context['list_url'] = self.success_url
        return context
