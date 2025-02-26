import json
from django.utils.deprecation import MiddlewareMixin

class CookieConsentMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Always allow essential cookies
        request.has_analytics_consent = True 
        request.has_marketing_consent = False

        cookie_consent = request.COOKIES.get('cookie_consent')
        if cookie_consent:
            consent_data = json.loads(cookie_consent)
            request.has_analytics_consent = consent_data.get('analytics', True)
            request.has_marketing_consent = consent_data.get('marketing', False)

    def process_response(self, request, response):
        return response
    