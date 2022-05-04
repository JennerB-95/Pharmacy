from django.urls import path
from core.erp.views.category.views import *
from core.erp.views.laboratory.views import *
from core.erp.views.distribuidor.views import *
from core.erp.views.unit.views import *
from core.erp.views.client.views import *
from core.erp.views.dashboard.views import *
from core.erp.views.product.views import *
from core.erp.views.shopping.views import *
from core.erp.views.sale.views import *
from core.erp.views.tests.views import TestView

app_name = 'erp'

urlpatterns = [
    # category
    path('category/list/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # laboratory
    path('laboratory/list/', LaboratoryListView.as_view(), name='laboratory_list'),
    path('laboratory/add/', LaboratoryCreateView.as_view(), name='laboratory_create'),
    path('laboratory/update/<int:pk>/', LaboratoryUpdateView.as_view(), name='laboratory_update'),
    path('laboratory/delete/<int:pk>/', LaboratoryDeleteView.as_view(), name='laboratory_delete'),
    # distribuidor
    path('distribuidor/list/', DistribuidorListView.as_view(), name='distribuidor_list'),
    path('distribuidor/add/', DistribuidorCreateView.as_view(), name='distribuidor_create'),
    path('distribuidor/update/<int:pk>/', DistribuidorUpdateView.as_view(), name='distribuidor_update'),
    path('distribuidor/delete/<int:pk>/', DistribuidorDeleteView.as_view(), name='distribuidor_delete'),
    # Unit
    path('unit/list/', UnitListView.as_view(), name='unit_list'),
    path('unit/add/', UnitCreateView.as_view(), name='unit_create'),
    path('unit/update/<int:pk>/', UnitUpdateView.as_view(), name='unit_update'),
    path('unit/delete/<int:pk>/', UnitDeleteView.as_view(), name='unit_delete'),
    # client
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    # product
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # test
    path('test/', TestView.as_view(), name='test'),
    # shopping
    path('shopping/list/', ShoppingListView.as_view(), name='shopping_list'),
    path('shopping/add/', ShoppingCreateView.as_view(), name='shopping_create'),
    path('shopping/delete/<int:pk>/', ShoppingDeleteView.as_view(), name='shopping_delete'),
    path('shopping/update/<int:pk>/', ShoppingUpdateView.as_view(), name='shopping_update'),
    path('shopping/invoice/pdf/<int:pk>/', ShoppingInvoicePdfView.as_view(), name='shopping_invoice_pdf'),
    # sale
    path('sale/list/', SaleListView.as_view(), name='sale_list'),
    path('sale/add/', SaleCreateView.as_view(), name='sale_create'),
    path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('sale/update/<int:pk>/', SaleUpdateView.as_view(), name='sale_update'),
    path('sale/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),
    #api
    path('api/due_date', Product_Due.as_view(), name="due_date"), 

]
