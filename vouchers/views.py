import io
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from pet_businesses.utils import group_required
from django.utils.timezone import now
from datetime import timedelta
from .models import Voucher
from pet_businesses.models import PetBusiness
from django.contrib.auth.models import User

@group_required("Pet Owners")
def generate_single_voucher(request, business_id, discount_type):
    """Generate a single voucher (50% or 20 CHF) as a PDF from an HTML template."""

    # Retrieve the business linked to the provided ID
    business = get_object_or_404(PetBusiness, id=business_id)

    # The voucher is now linked to the User instead of PetOwner
    user = request.user  

    # Check if the voucher for this discount type already exists
    existing_voucher = Voucher.objects.filter(
        user=user,  
        pet_business=business,
        discount_type=discount_type
    ).first()

    if existing_voucher:
        # If it exists, use the stored PDF
        if existing_voucher.pdf_file:
            response = HttpResponse(existing_voucher.pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="voucher_{existing_voucher.code}.pdf"'
            return response
        return HttpResponse("PDF not available for this voucher.", status=404)

    # Generate the single voucher if it doesn’t exist
    date_expires = now() + timedelta(days=90)

    if discount_type == 'percentage':
        voucher = Voucher(
            pet_business=business,
            user=user, 
            discount_type='percentage',
            discount_value=50.00,
            date_expires=date_expires
        )
    elif discount_type == 'fixed':
        voucher = Voucher(
            pet_business=business,
            user=user, 
            discount_type='fixed',
            discount_value=20.00,
            date_expires=date_expires
        )
    else:
        return HttpResponse("Invalid discount type.", status=400)

    voucher.save()  # This triggers code generation via the save method

    # Generate the PDF
    html_string = render_to_string('vouchers/voucher_pdf.html', {'vouchers': [voucher]})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="voucher_{voucher.code}.pdf"'
    HTML(string=html_string).write_pdf(response)

    # Save the PDF to the voucher (new path: media/vouchers/)
    individual_buffer = io.BytesIO()
    HTML(string=html_string).write_pdf(individual_buffer)
    voucher.pdf_file.save(f"vouchers/voucher_{voucher.code}.pdf", ContentFile(individual_buffer.getvalue()))  
    voucher.save()
    individual_buffer.close()

    return response
