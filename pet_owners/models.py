from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class PetOwner(models.Model):
    """
    Model representing a pet owner with personal information 
    for invoices and mailings.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pet_owners"
    )
    street=models.CharField(max_length=80, null=False, blank=False)
    street_number=models.CharField(max_length=10, null=False, blank=False)
    postal_code=models.CharField(max_length=10, null=False, blank=False)
    city = models.CharField(max_length=40, null=False, blank=False)
    country = models.CharField(max_length=80, null=True, blank=True, default="Suisse")
    phone = models.CharField(max_length=16, blank=True, null=True)
    newsletter = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pet Owner"
        verbose_name_plural = "Pet Owners"

    def __str__(self):
        return f"{self.author.username} - {self.city}"


class Pet(models.Model):
    """
    Model representing the pets owned by pet owners.
    """
    pet_owner = models.ForeignKey(
        PetOwner,
        on_delete=models.CASCADE,
        related_name="pets"
    )
    name = models.CharField(max_length=150)
    birthday = models.DateField(blank=True, null=True)
    pet_type = models.ForeignKey(
        "pet_businesses.PetType",
        on_delete=models.SET_NULL,
        related_name="pets",
        null=True,
        blank=True
    )
    pet_featured_image = CloudinaryField('image', default='placeholder')
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Pet"
        verbose_name_plural = "Pets"

    def __str__(self):
        return f"{self.name}"
