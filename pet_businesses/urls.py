from . import views
from django.urls import path
from .views import ajax_like_toggle

urlpatterns = [
     path('', views.BusinessList.as_view(), name='home'),
     path('pet_business_form/', views.pet_business_form,
          name='pet_business_form'),
     path('<slug:slug>/', views.pet_business_detail,
          name='pet_business_detail'),
     path('<slug:slug>/edit_comment/<int:comment_id>',
          views.comment_edit, name='comment_edit'),
     path('<slug:slug>/delete_comment/<int:comment_id>/',
          views.comment_delete, name='comment_delete'),
     path('<slug:slug>/edit/<int:pet_business_id>/',
          views.pet_business_edit, name='pet_business_edit'),
     path('<slug:slug>/delete/<int:pet_business_id>/',
          views.pet_business_delete, name='pet_business_delete'),
     path('ajax/like-toggle/', ajax_like_toggle, name='ajax_like_toggle'),
]
