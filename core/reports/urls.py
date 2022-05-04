from django.urls import path

from core.reports.views import ReportSaleView, ReportShoppingView, ReportEarningView

urlpatterns = [
    # reports
    path('sale/', ReportSaleView.as_view(), name='sale_report'),
    path('shopping/', ReportShoppingView.as_view(), name='shopping_report'),
    path('earning/', ReportEarningView.as_view(), name='earning_report'),
]