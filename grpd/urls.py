from django.urls import path
from .views import LegalNoticeView, CookiesNoticeView, PrivacyPolicyView

urlpatterns = [
    path('mentions-legales/', LegalNoticeView.as_view(), name='legal_notice'),
    path('notice-cookies/', CookiesNoticeView.as_view(), name='cookies_notice'),
    path('politique-confidentialite/', PrivacyPolicyView.as_view(), name='privacy_policy'),
]
