from django.urls import path
from . import views

app_name = 'vouchers'

urlpatterns = [
    path('generate/<int:business_id>/', views.generate_vouchers, name='generate_vouchers'),
    path('generate/<int:business_id>/<str:discount_type>/', views.generate_single_voucher, name='generate_single_voucher'),
    path('list/', views.voucher_list, name='voucher_list'),
    path('<int:voucher_id>/', views.voucher_detail, name='voucher_detail'),
    path('download/<int:voucher_id>/', views.download_voucher_pdf, name='download_voucher_pdf'),
]
