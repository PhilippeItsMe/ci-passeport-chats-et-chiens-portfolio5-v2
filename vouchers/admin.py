from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Voucher

@admin.register(Voucher)
class VoucherAdmin(SummernoteModelAdmin):
    list_display = (
        'user', 'pet_business', 'discount_type', 'date_created', 'date_expires'
    )
    list_filter = ('discount_type', 'date_expires', 'pet_business')
    search_fields = ('code',)

    ordering = ('-date_created',)

    def has_add_permission(self, request):
        """Prevents manual addition of vouchers via the admin interface."""
        return False  # Only created through the system
    