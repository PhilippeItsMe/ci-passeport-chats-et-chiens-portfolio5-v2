import uuid
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from products.models import Product
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta


COUNTRY_CHOICES = [
    ('CH', 'Suisse'),
    ('LI', 'Liechtenstein'),
]


class Order(models.Model):
    """
    Model to represent the order.
    """
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True,
    )

    full_name = models.CharField(max_length=50, null=False, blank=False)
    street = models.CharField(max_length=80, null=False, blank=False)
    postal_code = models.CharField(max_length=10, null=False, blank=False)
    city = models.CharField(max_length=40, null=False, blank=False)
    country = models.CharField(max_length=80, null=False, blank=False,
                               choices=COUNTRY_CHOICES, default="CH")
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone = models.CharField(max_length=16, blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True)
    total_ttc = models.DecimalField(max_digits=10, decimal_places=2,
                                    null=False, default=0)
    # Stores the original cart (JSON)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254,
                                  null=False, blank=False, default='')

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-date']

    def _generate_order_number(self):
        """Generate a random, unique order number using UUID"""
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """Update total_ttc each time a line item is added or changed"""
        self.total_ttc = self.lineitems.aggregate(
            Sum('lineitem_total')
        )['lineitem_total__sum'] or 0
        self.save()

    def save(self, *args, **kwargs):
        """Set order number on first save"""
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """
    Model to represent line items.
    """
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='lineitems'
    )
    product = models.ForeignKey(
        Product,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=10,
                                         decimal_places=2, null=False,
                                         blank=False, editable=False)

    class Meta:
        verbose_name = "Order Line Item"
        verbose_name_plural = "Order Line Items"

    def save(self, *args, **kwargs):
        """
        Calculate line item total and update order's total automatically.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)
        self.order.update_total()

    def __str__(self):
        return f"{self.product.name} on order {self.order.order_number}"


class ActivationCode(models.Model):
    """
    Model to represent activation code.
    """
    order_line_item = models.ForeignKey(
        'OrderLineItem',
        on_delete=models.CASCADE,
        related_name='orderlineitem_activation_code'
    )
    activation_code = models.CharField(
        max_length=10,
        unique=True,
        editable=False
    )
    date_created = models.DateTimeField(auto_now_add=True)

    activation_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    activated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='activated_codes'
    )

    def __str__(self):
        return f"{self.activation_code} for {self.order_line_item}"

    def activate(self, user):
        """Active le code pour 365 jours à partir d'aujourd'hui."""
        if not self.is_active:
            self.activation_date = timezone.now()
            self.is_active = True
            self.activated_by = user
            self.save()

    def is_expired(self):
        """Retourne True si le code est activé et expiré."""
        if self.is_active and self.activation_date:
            return timezone.now() > self.activation_date + timedelta(days=365)
        return False

    @staticmethod
    def generate_unique_activation_code():
        """Generate a unique 10-digit numeric activation code."""
        while True:
            code = get_random_string(length=10, allowed_chars='0123456789')
            if not ActivationCode.objects.filter(activation_code=code
                                                 ).exists():

                return code
