from django.urls import path
from .views import BagView

urlpatterns = [
    path("bag/", BagView.as_view(), name="bag"),
]
