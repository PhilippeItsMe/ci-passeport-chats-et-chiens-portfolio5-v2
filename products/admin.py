from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'date_created',
                    'last_modified')
    search_fields = ('name', 'short_description')
    list_filter = ('date_created', 'last_modified')
    ordering = ('-date_created',)
