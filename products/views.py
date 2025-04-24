from django.shortcuts import render, get_object_or_404
from products.models import Product


def passeport_product_view(request):
    "View to add the product to the context"
    passeport_product = get_object_or_404(Product, name="Passeport 1 an")

    context = {
        "passeport_product": passeport_product,
    }

    return render(request, "base.html", context)
