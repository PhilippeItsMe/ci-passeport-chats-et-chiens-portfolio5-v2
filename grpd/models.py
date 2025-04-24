from django.db import models
from django.contrib.auth.models import User


class CookieConsent(models.Model):
    """
    Model do manage grpd consent
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)  # If logged
    session_key = models.CharField(
        max_length=255, null=True, blank=True)  # If not logged
    accepted_essential = models.BooleanField(default=True)
    accepted_analytics = models.BooleanField(default=False)
    accepted_marketing = models.BooleanField(default=False)
    date_consent_given = models.DateTimeField(auto_now_add=True)
