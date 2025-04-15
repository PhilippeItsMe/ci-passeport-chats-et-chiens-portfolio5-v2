from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('summernote/', include('django_summernote.urls')),


  # Email reset
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    
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
