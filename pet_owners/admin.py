from django.contrib import admin
from .models import PetOwner, Pet


@admin.register(PetOwner)
class PetOwnerAdmin(admin.ModelAdmin):
    """
    To display pet owners' personal info in admin.
    """
    list_display = (
        'author', 'default_street',
        'default_postal_code', 'default_city', 'default_country',
        'default_phone', 'default_newsletter',
        'default_last_modified', 'default_date_created'
    )
    search_fields = [
        'author__username', 'default_phone', 'default_street',
        'default_postal_code', 'default_city', 'default_country'
    ]
    list_filter = (
        'default_country', 'default_city',
        'default_date_created', 'default_last_modified'
    )
    ordering = ('-default_last_modified',)



@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    """
    To display pets in admin.
    """
    list_display = ('name', 'pet_owner', 'pet_type', 'birthday',
                    'last_modified', 'date_created')
    search_fields = ['name', 'pet_owner__author__username']
    list_filter = ('pet_type', 'date_created', 'last_modified')
