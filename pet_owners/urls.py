from . import views
from django.urls import path

urlpatterns = [
     path('pet_form/', views.pet_form,
          name='pet_form'),
     path('<slug:slug>/', views.pet,
          name='pet_detail'),
    path('<slug:slug>/edit/<int:pet_id>/',
         views.pet_business_edit, name='pet_edit'),
    path('<slug:slug>/delete/<int:pet_id>/',
         views.pet_business_delete, name='pet_delete'),
]
