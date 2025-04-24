from django.contrib import admin
from .models import Order, OrderLineItem, ActivationCode


class OrderLineItemAdminInline(admin.TabularInline):
    """
    To display line items in admin.
    """
    model = OrderLineItem
    extra = 0
    readonly_fields = ('lineitem_total', 'display_activation_codes')

    def display_activation_codes(self, obj):
        return ", ".join(code.activation_code for code in
                         obj.orderlineitem_activation_code.all())
    display_activation_codes.short_description = "Activation Codes"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    To display orders in admin.
    """
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = (
        'order_number', 'date', 'total_ttc',
        'original_bag', 'stripe_pid',
    )

    fields = (
        'order_number', 'user_profile', 'date',
        'full_name', 'street',
        'postal_code', 'city', 'country', 'phone', 'email',
        'total_ttc', 'original_bag', 'stripe_pid',
    )

    list_display = (
        'order_number', 'date', 'full_name',
        'total_ttc', 'city', 'country',
    )

    ordering = ('-date',)

    @admin.register(ActivationCode)
    class ActivationCodeAdmin(admin.ModelAdmin):
        """
        To display activation codes in admin.
        """
        list_display = (
            'activation_code',
            'order_line_item',
            'date_created',
            'activation_date',
            'is_active',
            'activated_by',
        )
        search_fields = (
            'activation_code',
            'order_line_item__order__order_number',
            'activated_by__email',
        )
        list_filter = (
            'date_created',
            'activation_date',
            'is_active',
        )
        autocomplete_fields = ('activated_by',)
