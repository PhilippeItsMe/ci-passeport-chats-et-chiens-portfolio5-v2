from django.utils.html import format_html
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Voucher

@admin.register(Voucher)
class VoucherAdmin(SummernoteModelAdmin):
    list_display = ('user', 'pet_business', 'discount_type', 'date_created', 'date_expires', 'pdf_link')
    list_filter = ('discount_type', 'date_expires', 'pet_business')
    search_fields = ('code',)
    ordering = ('-date_created',)
    readonly_fields = ('pdf_preview',)  # Show preview in the admin detail page

    def has_add_permission(self, request):
        """Prevents manual addition of vouchers via the admin interface."""
        return False  # Only created through the system

    def pdf_link(self, obj):
        """Display a link to download the voucher in the admin."""
        if obj.pdf_file and hasattr(obj.pdf_file, 'url'):
            return format_html('<a href="{}" target="_blank">📄 Télécharger</a>', obj.pdf_file.url)
        return "Aucun fichier"

    pdf_link.short_description = "Bon de réduction (PDF)"

    def pdf_preview(self, obj):
        """Display an embedded preview of the PDF in the admin detail page."""
        if obj.pdf_file and hasattr(obj.pdf_file, 'url'):
            return format_html('<embed src="{}" width="200px" height="300px" />', obj.pdf_file.url)
        return "No preview available"

    pdf_preview.short_description = "Aperçu du PDF"
