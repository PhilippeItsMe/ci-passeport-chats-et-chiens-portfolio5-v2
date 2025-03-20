from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_description = models.CharField(max_length=255)
    duration = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.price}€ - {self.duration} days"
