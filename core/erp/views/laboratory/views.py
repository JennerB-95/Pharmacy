from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import LaboratoryForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Laboratory


class LaboratoryListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Laboratory
    template_name = 'laboratory/list.html'
    permission_required = 'view_laboratory'

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
                for i in Laboratory.objects.all():
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
        context['title'] = 'Listado de Laboratorios'
        context['create_url'] = reverse_lazy('erp:laboratory_create')
        context['list_url'] = reverse_lazy('erp:laboratory_list')
        context['entity'] = 'Laboratorios'
        return context


class LaboratoryCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Laboratory
    form_class = LaboratoryForm
    template_name = 'laboratory/create.html'
    success_url = reverse_lazy('erp:laboratory_list')
    permission_required = 'add_laboratory'
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
        context['title'] = 'Crear Laboratorio'
        context['entity'] = 'Laboratorio'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class LaboratoryUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Laboratory
    form_class = LaboratoryForm
    template_name = 'laboratory/create.html'
    success_url = reverse_lazy('erp:laboratory_list')
    permission_required = 'change_laboratory'
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
        context['title'] = 'Editar Laboratorio'
        context['entity'] = 'Laboratorios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class LaboratoryDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Laboratory
    template_name = 'laboratory/delete.html'
    success_url = reverse_lazy('erp:laboratory_list')
    permission_required = 'delete_laboratory'
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
        context['title'] = 'Eliminar Laboratorio'
        context['entity'] = 'Laboratorios'
        context['list_url'] = self.success_url
        return context
