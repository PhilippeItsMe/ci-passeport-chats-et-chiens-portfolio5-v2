from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .models import Order, OrderLineItem, ActivationCode
from products.models import Product
from pet_owners.forms import PetOwnerForm
from pet_owners.models import PetOwner
from bag.contexts import bag_contents
from datetime import timedelta

import stripe
import json


@require_POST
def cache_checkout_data(request):
    """
    View to create the checkout session
    """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """
    View to manage checkout payement
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone': request.POST['phone'],
            'country': request.POST['country'],
            'postal_code': request.POST['postal_code'],
            'city': request.POST['city'],
            'street': request.POST['street'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items(
                        ):
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "L'un des articles commandés n'est pas dans notre dB."
                        "Merci de nous contacter pour de l'aide.")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(
                reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'Il y a une erreur avec votre formulaire. \
                Merci de vérifier vos informations.')
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(
                request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        total = current_bag['total_ttc']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                petowner = PetOwner.objects.get(author=request.user)
                order_form = OrderForm(initial={
                    'full_name': petowner.author.get_full_name(),
                    'email': petowner.author.email,
                    'phone': petowner.default_phone,
                    'country': petowner.default_country,
                    'postal_code': petowner.default_postal_code,
                    'city': petowner.default_city,
                    'street': petowner.default_street,
                })
            except PetOwner.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

        return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = PetOwner.objects.filter(author=request.user).first()

        if profile:
            # Attach the user's profile to the order
            order.user_profile = profile.author
            order.save()

            # Save the user's info
            if save_info:
                profile_data = {
                    'default_phone': order.phone,
                    'default_country': order.country,
                    'default_postal_code': order.postal_code,
                    'default_city': order.city,
                    'default_street': order.street,
                }
                user_profile_form = PetOwnerForm(
                    profile_data, instance=profile)
                if user_profile_form.is_valid():
                    user_profile_form.save()
        else:
            # Optionally, inform the user they should create their profile
            messages.info(
                request,
                "Merci de compléter votre profil "
                "pour sauvegarder vos informations de commande."
                )

    messages.success(request, f'Votre commande est bien passée! \
        Votre numéro de commande est {order_number}. Un email de \
        confirmation va être envoyé à {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)


@login_required
def order_history(request):
    """
    View to render order history
    """
    orders = Order.objects.filter(user_profile=request.user).order_by('-date')

    return render(request, 'checkout/order_history.html', {
        'orders': orders,
    })


def activation_code(request):
    user = request.user
    activation_code_input = request.POST.get('activation_code')
    context = {}

    # Vérifier si l'utilisateur a déjà un code actif non expiré
    user_active_code = ActivationCode.objects.filter(
        activated_by=user,
        is_active=True,
        activation_date__isnull=False
    ).order_by('-activation_date').first()

    if user_active_code and not user_active_code.is_expired():
        context['active_code'] = user_active_code
        context[
            'expiration_date'] = user_active_code.activation_date + timedelta(
                days=365)

    if request.method == 'POST' and activation_code_input:
        try:
            code = ActivationCode.objects.get(
                activation_code=activation_code_input)
        except ActivationCode.DoesNotExist:
            messages.error(request, "Ce code n'existe pas.")
            return redirect('activate_code')

        if code.is_active:
            messages.error(request, "Ce code est déjà activé.")
        elif code.is_expired():
            messages.error(request, "Ce code est expiré.")
        else:
            code.activate(user)
            messages.success(request, "Code activé avec succès !")
            return redirect('activate_code')

    return render(request, 'checkout/code_activation.html', context)
