from django.urls import path
from . import views

app_name = 'vouchers'

urlpatterns = [
    path('generate/<int:business_id>/<str:discount_type>/',
         views.generate_single_voucher, name='generate_single_voucher'),
]
