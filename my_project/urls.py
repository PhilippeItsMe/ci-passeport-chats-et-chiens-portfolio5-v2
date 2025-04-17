from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from my_project.views import TextOnlyPasswordResetView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),

    # Concept
     path('concept/', include('concept.urls')),  

     # Email reset
     path('password_reset/', TextOnlyPasswordResetView.as_view(),
          name='password_reset'),
     path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
          name='password_reset_done'),
     path('reset/<uidb64>/<token>/',
          auth_views.PasswordResetConfirmView.as_view(),
          name='password_reset_confirm'),
     path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
          name='password_reset_complete'),
     
     # Account
     path('accounts/', include('allauth.urls')),
    
     # BAG
     path('bag/', include('bag.urls')),

     # Checkout
     path('checkout/', include('checkout.urls')),

     # Pet Owners
     path('', include('pet_owners.urls')),

     # Pet Businesses
     path('', include('pet_businesses.urls')),

     # Vouchers
     path('vouchers/', include('vouchers.urls')),

     # GRPD
     path('grpd/', include('grpd.urls')),

     # Products
     path('products/', include('products.urls')),   
]

handler404 = 'my_project.views.handler404'
