from django.views.generic import TemplateView

class LegalNoticeView(TemplateView):
    template_name = "legal_notice.html"

class CookiesNoticeView(TemplateView):
    template_name = "cookies_notice.html"

class PrivacyPolicyView(TemplateView):
    template_name = "privacy_policy.html"
