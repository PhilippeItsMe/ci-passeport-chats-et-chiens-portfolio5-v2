from django.urls import path
from . import views

urlpatterns = [
    path('pet_owner_form/', views.pet_owner_form, name='pet_owner_form'),
    path('pets/', views.pet_list, name='pet_list'),    
    path('pets/add/', views.pet_create, name='pet_create'),      
    path('pets/<int:pet_id>/edit/', views.pet_edit, name='pet_edit'),
    path('pets/<int:pet_id>/delete/', views.pet_delete, name='pet_delete'),
]
