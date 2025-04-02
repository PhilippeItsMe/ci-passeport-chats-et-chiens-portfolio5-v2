from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('summernote/', include('django_summernote.urls')),
    
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
