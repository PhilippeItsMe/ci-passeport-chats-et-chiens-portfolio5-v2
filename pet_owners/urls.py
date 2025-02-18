from django.urls import path
from . import views

urlpatterns = [
    path('pet_owner_form/', views.pet_owner_form, name='pet_owner_form'),
    path('pets/add/', views.pet_create, name='pet-create'),      
    path('pets/<int:pet_id>/edit/', views.pet_edit, name='pet-edit'),
    path('pets/<int:pet_id>/delete/', views.pet_delete, name='pet-delete'),
]
