from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.pet_owner_form, name='petowner-detail'),
    path('pets/add/', views.pet_create, name='pet-create'),      
    path('pets/<int:pet_id>/edit/', views.pet_edit, name='pet-edit'),
    path('pets/<int:pet_id>/delete/', views.pet_delete, name='pet-delete'),
]
