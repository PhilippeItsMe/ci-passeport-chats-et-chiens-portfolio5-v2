from django.db import models
from django.contrib.auth.models import User
from pet_businesses.models import PetBusiness
from pet_owners.models import PetOwner
import random
import string
from django.utils.timezone import now
from datetime import timedelta

class Voucher(models.Model):
    """
    Model representing vouchers for discounts on pet businesses.
    Two vouchers per business: one 50% off and one 20 CHF off.
    Includes a PDF file for the downloaded voucher.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),  # After 90 days
    ]
    
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]

    pet_business = models.ForeignKey(
        PetBusiness,
        on_delete=models.CASCADE,
        related_name='vouchers'
    )
    pet_owner = models.ForeignKey(
        PetOwner,
        on_delete=models.CASCADE,
        related_name='vouchers'
    )
    code = models.CharField(max_length=12, unique=True, editable=False)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=6, decimal_places=2)  # 50.00 pour % ou 20.00 pour CHF
    minimum_purchase = models.DecimalField(max_digits=6, decimal_places=2, default=100.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    date_created = models.DateTimeField(auto_now_add=True)
    date_expires = models.DateTimeField()
    pdf_file = models.FileField(upload_to='vouchers/pdfs/', null=True, blank=True)  #In case of dispute

    class Meta:
        ordering = ['-date_created']
        verbose_name = "Voucher"
        verbose_name_plural = "Vouchers"
        constraints = [
            models.UniqueConstraint(
                fields=['pet_owner', 'pet_business', 'discount_type'],
                name='unique_voucher_per_business'
            )
        ]

    def __str__(self):
        return f"Voucher {self.code} for {self.pet_business.firm} - {self.pet_owner.author.username}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self._generate_unique_code()
        super().save(*args, **kwargs)

    def _generate_unique_code(self):
        """Generate a unique code per voucher."""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            if not Voucher.objects.filter(code=code).exists():
                return code

    def get_full_details(self):
        """
        Returns formatted voucher details including business and owner information.
        """
        discount_text = (
            f"{self.discount_value}%" if self.discount_type == 'percentage'
            else f"CHF {self.discount_value}"
        )
        return (
            f"Voucher Code: {self.code}\n"
            f"Business: {self.pet_business.firm}\n"
            f"Address: {self.pet_business.street} {self.pet_business.number}, "
            f"{self.pet_business.npa} {self.pet_business.locality}\n"
            f"Pet Owner: {self.pet_owner.author.first_name} {self.pet_owner.author.last_name}\n"
            f"Discount: {discount_text} off\n"
            f"Minimum Purchase: CHF {self.minimum_purchase}\n"
            f"Expires: {self.date_expires.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    @classmethod
    def create_vouchers_for_business(cls, pet_business, pet_owner):
        """Automatically create the vouchers."""
        vouchers = []
        
        # Voucher 50%
        percentage_voucher = cls(
            pet_business=pet_business,
            pet_owner=pet_owner,
            discount_type='percentage',
            discount_value=50.00, # 50% set up
            date_expires = now() + timedelta(days=90) # Duration set up
        )
        percentage_voucher.save()
        vouchers.append(percentage_voucher)

        # Voucher 20 CHF
        fixed_voucher = cls(
            pet_business=pet_business,
            pet_owner=pet_owner,
            discount_type='fixed',
            discount_value=20.00, # CHF set up
            date_expires = now() + timedelta(days=90) # Duration set up
        )
        fixed_voucher.save()
        vouchers.append(fixed_voucher)

        return vouchers
    