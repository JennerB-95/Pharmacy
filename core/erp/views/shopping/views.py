import json
import os

from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, View
from xhtml2pdf import pisa

from core.erp.forms import ShoppingForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Shopping, Product, DetShopping


class ShoppingListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Shopping
    template_name = 'shopping/list.html'
    permission_required = 'view_shopping'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Shopping.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in DetShopping.objects.filter(shopping_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Compras'
        context['create_url'] = reverse_lazy('erp:shopping_create')
        context['list_url'] = reverse_lazy('erp:shopping_list')
        context['entity'] = 'Compras'
        return context


class ShoppingCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Shopping
    form_class = ShoppingForm
    template_name = 'shopping/create.html'
    success_url = reverse_lazy('erp:shopping_list')
    permission_required = 'add_shopping'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Product.objects.filter(barcode__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    # item['value'] = i.name
                    item['text'] = i.name
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    shoppings = json.loads(request.POST['shoppings'])
                    shopping = Shopping()
                    shopping.date_joined = shoppings['date_joined']
                    shopping.laboratory_id = shoppings['laboratory']
                    shopping.no_bill = shoppings['no_bill']
                    shopping.subtotal = float(shoppings['subtotal'])
                    shopping.total = float(shoppings['total'])
                    shopping.save()
                    for i in shoppings['products']:
                        det = DetShopping()
                        det.shopping_id = shopping.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp_cmp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    data = {'id': shopping.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Compra'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        return context


class ShoppingUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Shopping
    form_class = ShoppingForm
    template_name = 'shopping/create.html'
    success_url = reverse_lazy('erp:shopping_list')
    permission_required = 'change_shopping'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Product.objects.filter(barcode__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.name
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    shoppings = json.loads(request.POST['shoppings'])
                    # shopping = Shopping.objects.get(pk=self.get_object().id)
                    shopping = self.get_object()
                    shopping.date_joined = shoppings['date_joined']
                    shopping.laboratory_id = shoppings['laboratory']
                    shopping.no_bill = shoppings['no_bill']
                    shopping.subtotal = float(shoppings['subtotal'])
                    shopping.total = float(shoppings['total'])
                    shopping.save()
                    shopping.detshopping_set.all().delete()
                    for i in shoppings['products']:
                        det = DetShopping()
                        det.shopping_id = shopping.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp_cmp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    data = {'id': shopping.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in DetShopping.objects.filter(shopping_id=self.get_object().id):
                item = i.prod.toJSON()
                item['cant'] = i.cant
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Compra'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product(), cls=DjangoJSONEncoder)
        return context


class ShoppingDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Shopping
    template_name = 'shopping/delete.html'
    success_url = reverse_lazy('erp:shopping_list')
    permission_required = 'delete_shopping'
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
        context['title'] = 'Eliminar Compra'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        return context


class ShoppingInvoicePdfView(View):

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('shopping/invoice.html')
            context = {
                'shopping': Shopping.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'ALL SAFE SECURITY & TECHNOLOGY S.A.', 'ruc': '30402185', 'address': 'Guatemala, Guatemala'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:shopping_list'))