from django.views.generic import TemplateView

class LegalNoticeView(TemplateView):
    template_name = "grpd/legal_notice.html"

class CookiesNoticeView(TemplateView):
    template_name = "grpd/cookies_notice.html"

class PrivacyPolicyView(TemplateView):
    template_name = "grpd/privacy_policy.html"
    