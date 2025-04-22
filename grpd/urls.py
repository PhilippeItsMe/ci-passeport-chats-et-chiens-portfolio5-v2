from django.urls import path
from .views import PrivacyPolicyView,CGV, save_cookie_consent
from .views import LegalNoticeView, CookiesNoticeView

urlpatterns = [
    path('conditions-generales-de-vente/', CGV.as_view(), name='cgv'),
    path('mentions-legales/', LegalNoticeView.as_view(), name='legal_notice'),
    path('notice-cookies/', CookiesNoticeView.as_view(), name='cookies_notice'),
    path('politique-confidentialite/',
         PrivacyPolicyView.as_view(), name='privacy_policy'),
    path("save-cookie-consent/",
         save_cookie_consent, name="save_cookie_consent"),
]
