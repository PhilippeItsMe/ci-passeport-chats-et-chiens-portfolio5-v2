from django.contrib import admin
from .models import PetBusiness, ServiceType, PetType, Comment, Like
from django_summernote.admin import SummernoteModelAdmin


@admin.register(PetBusiness)
class PostAdmin(SummernoteModelAdmin):
    """
    To display pet businesses in admin.
    """
    list_display = ('firm', 'locality', 'approved',
                    'last_modified', 'date_created')
    search_fields = ['firm', 'locality']
    prepopulated_fields = {'slug': ('firm',)}
    summernote_fields = ('description',)

    def save_model(self, request, obj, form, change):
        """
        Override save_model to handle Many-to-Many fields explicitly.
        """
        super().save_model(request, obj, form, change)
        # Save Many-to-Many fields explicitly
        form.save_m2m()


@admin.register(ServiceType)
class PostAdmin(SummernoteModelAdmin):
    """
    To display service types in admin.
    """
    list_display = ('service_type', 'date_created')


@admin.register(PetType)
class PostAdmin(SummernoteModelAdmin):
    """
    To display pet types in admins
    """
    list_display = ('pet_type', 'date_created')


@admin.register(Comment)
class PostAdmin(SummernoteModelAdmin):
    """
    To display comments in admins
    """
    list_display = ('pet_businesse', 'author', 'approved',
                    'last_modified', 'date_created')


@admin.register(Like)
class PostAdmin(SummernoteModelAdmin):
    """
    To display likes in admin.
    """
    list_display = ('pet_business', 'author', 'date_created')
