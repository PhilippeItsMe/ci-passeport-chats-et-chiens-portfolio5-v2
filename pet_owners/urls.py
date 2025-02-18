from . import views
from django.urls import path

urlpatterns = [
    # PetOwner URLs
    path('profile/create/', views.PetOwnerCreateView.as_view(), 
         name='petowner-create'),
    path('profile/', views.PetOwnerDetailView.as_view(), 
         name='petowner-detail'),
    path('profile/edit/', views.PetOwnerUpdateView.as_view(), 
         name='petowner-update'),

    # Pet URLs
    path('pets/add/', views.PetCreateView.as_view(), name='pet-create'),
    path('pets/<int:pk>/edit/', views.PetUpdateView.as_view(), 
         name='pet-update'),
    path('pets/<int:pk>/delete/', views.PetDeleteView.as_view(), 
         name='pet-delete'),
]
