from django.urls import path
from . import views

app_name = 'vouchers'

urlpatterns = [
    path('generate/<int:business_id>/', views.generate_vouchers, name='generate_vouchers'),
    path('list/', views.voucher_list, name='voucher_list'),
    path('<int:voucher_id>/', views.voucher_detail, name='voucher_detail'),
]
