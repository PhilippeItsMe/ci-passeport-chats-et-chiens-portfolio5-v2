from django.contrib import admin
from .models import PetOwner, Pet
from django_summernote.admin import SummernoteModelAdmin


@admin.register(PetOwner)
class PetOwnerAdmin(admin.ModelAdmin):
    """
    To display pet owners in admin.
    """
    list_display = ('author', 'phone', 'newsletter',
                    'last_modified', 'date_created')
    search_fields = ['author__username', 'phone']
    list_filter = ('newsletter', 'date_created', 'last_modified')


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    """
    To display pets in admin.
    """
    list_display = ('name', 'pet_owner', 'pet_type', 'birthday',
                    'last_modified', 'date_created')
    search_fields = ['name', 'pet_owner__author__username']
    list_filter = ('pet_type', 'date_created', 'last_modified')
