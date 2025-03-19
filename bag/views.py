from django.views.generic import TemplateView

class BagView(TemplateView):
    template_name = "bag/bag.html"
    