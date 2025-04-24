from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem, ActivationCode
from products.models import Product
from pet_owners.models import PetOwner

import json
import time
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeWH_Handler:
    """Handle Stripe webhooks"""
    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        activation_codes = ActivationCode.objects.filter(
            order_line_item__order=order)

        original_bag = json.loads(order.original_bag)
        total_quantity = sum(original_bag.values())

        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})

        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order,
             'total_quantity': total_quantity,
             'activation_codes': activation_codes,
             'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info
        # print ('debug intent:', intent)
        charge = stripe.Charge.retrieve(intent.latest_charge)
        # print ('debug charge:', charge)
        billing_details = charge.billing_details
        total_ttc = round(charge.amount / 100, 2)

        # Clean data in the shipping details
        for field, value in billing_details.address.items():
            if value == "":
                billing_details.address[field] = None

        # Update profile information if save_info was checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = PetOwner.objects.get(user__username=username)
            if save_info:
                profile.default_street = billing_details.address.line1
                profile.default_postal_code = billing_details.address.postal_code
                profile.default_city = billing_details.address.city
                profile.default_country = billing_details.address.country
                profile.default_phone = billing_details.phone
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=billing_details.name,
                    street__iexact=billing_details.address.line1,
                    postal_code__iexact=billing_details.address.postal_code,
                    city__iexact=billing_details.address.city,
                    country__iexact=billing_details.address.country,
                    email__iexact=billing_details.email,
                    phone__iexact=billing_details.phone,
                    total_ttc=total_ttc,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {
                    event["type"]
                    } | SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    user_profile=profile,
                    full_name=billing_details.name,
                    street=billing_details.address.line1,
                    postal_code=billing_details.address.postal_code,
                    city=billing_details.address.city,
                    country=billing_details.address.country,
                    email=billing_details.email,
                    phone=billing_details.phone,
                    total_ttc=total_ttc,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                for item_id, item_data in json.loads(bag).items():
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'
                                                        ].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event[
                "type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
