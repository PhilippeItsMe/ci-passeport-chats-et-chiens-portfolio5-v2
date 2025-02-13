from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path('accounts/', include('pet_businesses.urls')),
    path('summernote/', include('django_summernote.urls')),
    path("", include("pet_businesses.urls"), name="pet_businesses_urls"),
]
