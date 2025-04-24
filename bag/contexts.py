from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    bag_items = []
    total_ttc = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        total_ttc += quantity * product.price
        product_count += quantity
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    TVA_RATE = 8.1 / 100
    total_ht = float(total_ttc) / (1 + TVA_RATE)  # Total before VAT (100%)
    tva = total_ht * TVA_RATE  # VAT amount (8.1%)

    context = {
        'bag_items': bag_items,
        'product_count': product_count,
        'total_ttc': total_ttc,
        'total_ht': round(total_ht, 2),
        'tva': round(tva, 2),
    }

    return context
