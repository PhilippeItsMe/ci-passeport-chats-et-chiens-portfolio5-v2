from django.shortcuts import render, redirect, reverse, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from products.models import Product


def view_bag(request):
    """ A view that renders the bag contents page """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    print('item_id', item_id)
    print('request', request)
    print('request.session:', dict(request.session))

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity',
                                    1))  # Default quantity to 1
    redirect_url = request.POST.get('redirect_url') or reverse('bag:view_bag')
    bag = request.session.get('bag', {})

    item_id = str(item_id)  # Ensure consistency in session storage

    if item_id in bag:
        bag[item_id] += quantity
        messages.success(request,
                         f'Le nombre de "{product.name}" a été adapté.')
    else:
        bag[item_id] = quantity
        messages.success(request,
                         f'"{product.name}" a été ajouté à votre panier.')

    request.session['bag'] = bag

    print('request.session après:', dict(request.session))

    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust the quantity of specified product to specified amount """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity',
                                    1))  # Default quantity 1 if not provided
    bag = request.session.get('bag', {})
    item_id = str(item_id)  # Convert to string for consistency

    if quantity > 0:
        bag[item_id] = quantity
        messages.success(request,
                         f'Le nombre de "{product.name}" a été adapté.')
    else:
        bag.pop(item_id, None)  # Avoid KeyError
        messages.success(request,
                         f'"{product.name}" a été enlevé de votre panier.')

    request.session['bag'] = bag
    return redirect(reverse('bag:view_bag'))


def remove_from_bag(request, item_id):
    """ Remove the item from the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    bag = request.session.get('bag', {})

    item_id = str(item_id)  # Convert to string for consistency

    if item_id in bag:
        bag.pop(item_id, None)
        messages.success(request,
                         f'"{product.name}" a été enlevé de votre panier.')
    request.session['bag'] = bag

    return HttpResponse(status=200)
