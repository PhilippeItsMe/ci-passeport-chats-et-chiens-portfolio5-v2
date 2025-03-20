from django.urls import path
from .views import passeport_product_view  # Ensure this import is correct

urlpatterns = [
    path("passeport/", passeport_product_view, name="passeport_product"),
]
