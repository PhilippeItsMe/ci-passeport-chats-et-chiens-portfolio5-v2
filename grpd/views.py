from django.views.generic import TemplateView
import json
from django.http import JsonResponse
from .models import CookieConsent


class LegalNoticeView(TemplateView):
    """
    View to render legal notice. 
    """
    template_name = "grpd/legal_notice.html"


class CookiesNoticeView(TemplateView):
    """
    View to render cookies notive.
    """
    template_name = "grpd/cookies_notice.html"


class PrivacyPolicyView(TemplateView):
    """
    View to render privacy policy.
    """
    template_name = "grpd/privacy_policy.html"


def save_cookie_consent(request):
    """
    View to save conset cookies.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            analytics = data.get("analytics", False)
            marketing = data.get("marketing", False)

            # Get session key if user is not logged in
            session_key = request.session.session_key or request.session.create()
            
            if request.user.is_authenticated:
                # Store consent for logged-in user
                consent, created = CookieConsent.objects.get_or_create(user=request.user)
            else:
                # Store consent for anonymous user
                consent, created = CookieConsent.objects.get_or_create(session_key=session_key)

            # Update fields
            consent.accepted_analytics = analytics
            consent.accepted_marketing = marketing
            consent.save()

            return JsonResponse({"message": "Consent saved successfully"})
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid data"}, status=400)
    