from django.utils.html import format_html
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Voucher

@admin.register(Voucher)
class VoucherAdmin(SummernoteModelAdmin):
    list_display = (
        'user', 'pet_business', 'discount_type', 'date_created', 'date_expires', 'pdf_link'
    )
    list_filter = ('discount_type', 'date_expires', 'pet_business')
    search_fields = ('code',)
    ordering = ('-date_created',)

    def has_add_permission(self, request):
        return False  # Prevent manual addition of vouchers

    def pdf_link(self, obj):
        """Display a link to download the voucher in the admin."""
        if obj.pdf_file:
            return format_html('<a href="{}" target="_blank">📄 Télécharger</a>', obj.pdf_file)
        return "Aucun fichier"

    pdf_link.short_description = "Bon de réduction (PDF)"
