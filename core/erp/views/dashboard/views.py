from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView
from rest_framework.views import APIView 
from rest_framework.response import Response


from core.erp.models import Sale, Product, DetSale, Client

from random import randint


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_graph_sales_year_month':
                data = {
                    'name': 'Porcentaje de venta',
                    'showInLegend': False,
                    'colorByPoint': True,
                    'data': self.get_graph_sales_year_month()
                }
            elif action == 'get_graph_sales_products_year_month':
                data = {
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': self.get_graph_sales_products_year_month(),
                }
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_graph_sales_year_month(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 13):
                total = Sale.objects.filter(date_joined__year=year, date_joined__month=m).aggregate(
                    r=Coalesce(Sum('total'), 0)).get('r')
                data.append(float(total))
        except:
            pass
        return data

    def get_graph_sales_products_year_month(self):
        data = []
        year = datetime.now().year
        month = datetime.now().month
        try:
            for p in Product.objects.all():
                total = DetSale.objects.filter(sale__date_joined__year=year, sale__date_joined__month=month,
                                               prod_id=p.id).aggregate(
                    r=Coalesce(Sum('subtotal'), 0)).get('r')
                if total > 0:
                    data.append({
                        'name': p.name,
                        'y': float(total)
                    })
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prod'] = Product.objects.all()
        context['products'] = Product.objects.filter().count()
        context['clients']  = Client.objects.filter().count()
        result_list = []
        memberList = Product.objects.filter()
        for item in memberList:
            if item.stock_label == 'Danger':
                result_list.append(item)
        context['alertas'] = len(result_list)

        context['title'] = 'Panel de administrador'
        context['graph_sales_year_month'] = self.get_graph_sales_year_month()
        return context


class Product_Due(APIView):
    def get(self, request, format=None):
        data = []
        queryset = Product.objects.order_by('due_date')[:5]
        for product in queryset: 

            data.append({
                "description": product.name,
                "laboratory": product.lab.description,
                "due_date": product.due_date,
                "stock": product.stock
            })        
        return Response(data)