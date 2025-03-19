from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Nom unique du produit
    short_description = models.CharField(max_length=255)  # Courte description
    duration = models.PositiveIntegerField()  # Durée en jours
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Prix du produit
    date_created = models.DateTimeField(auto_now_add=True)  # Date de création
    last_modified = models.DateTimeField(auto_now=True)  # Dernière modification

    def __str__(self):
        return f"{self.name} - {self.price}€ - {self.duration} days"
