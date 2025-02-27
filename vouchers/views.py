import io
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.utils.timezone import now
from datetime import timedelta
from .models import Voucher
from pet_businesses.models import PetBusiness
from pet_businesses.utils import group_required

@group_required("Pet Owners")
def generate_single_voucher(request, business_id, discount_type):
    """Generate a single voucher (50% or 20 CHF) as a PDF and store in Cloudinary."""

    # Retrieve the business linked to the provided ID
    business = get_object_or_404(PetBusiness, id=business_id)
    user = request.user  

    # Check if the voucher already exists
    existing_voucher = Voucher.objects.filter(
        user=user,  
        pet_business=business,
        discount_type=discount_type
    ).first()

    if existing_voucher and existing_voucher.pdf_file:
        return HttpResponse(existing_voucher.pdf_file.url, content_type='application/pdf')

    # Validate discount type
    valid_discounts = {
        'percentage': 50.00,
        'fixed': 20.00
    }

    if discount_type not in valid_discounts:
        return HttpResponse("Invalid discount type.", status=400)

    # Create and save the voucher
    voucher = Voucher(
        pet_business=business,
        user=user, 
        discount_type=discount_type,
        discount_value=valid_discounts[discount_type],
        date_expires=now() + timedelta(days=90)
    )
    voucher.save()  # Ensure voucher has an ID before attaching the PDF

    # Generate the PDF
    html_string = render_to_string('vouchers/voucher_pdf.html', {'vouchers': [voucher]})
    pdf_buffer = io.BytesIO()
    HTML(string=html_string).write_pdf(pdf_buffer)

    # 🛠 Ensure PDF buffer is not empty before saving
    pdf_buffer.seek(0)  # Move the cursor back to the beginning
    if pdf_buffer.getbuffer().nbytes == 0:
        return HttpResponse("PDF generation failed.", status=500)

    # Save the PDF to Cloudinary
    pdf_filename = f"vouchers/voucher_{voucher.code}.pdf"
    try:
        voucher.pdf_file.save(pdf_filename, ContentFile(pdf_buffer.getvalue()))
        voucher.save()  # Save again to store the Cloudinary link
    except Exception as e:
        print(f"Error saving PDF to Cloudinary: {e}")  # Debugging
        return HttpResponse("Error saving voucher PDF.", status=500)

    # Serve the PDF as a response
    pdf_buffer.seek(0)
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
    return response
