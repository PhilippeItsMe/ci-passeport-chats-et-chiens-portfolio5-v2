from django.shortcuts import render
from django.views.generic import ListView

class BagView(ListView):
    template_name = "bag/bag.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    