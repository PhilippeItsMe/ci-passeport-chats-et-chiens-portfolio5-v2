from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = (
        'order_number', 'date', 'total_ttc',
        'original_bag', 'stripe_pid',
    )

    fields = (
        'order_number', 'user_profile', 'date',
        'full_name', 'street', 'street_number',
        'postal_code', 'city', 'country', 'phone','email'
        'total_ttc', 'original_bag', 'stripe_pid',
    )

    list_display = (
        'order_number', 'date', 'full_name',
        'total_ttc', 'city', 'country',
    )

    ordering = ('-date',)
