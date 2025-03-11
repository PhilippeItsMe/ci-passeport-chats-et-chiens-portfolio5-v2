import io
import base64
import random
import string
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from django.utils.timezone import now
from datetime import timedelta
from .models import Voucher
from pet_businesses.models import PetBusiness
from pet_businesses.utils import group_required
import cloudinary.uploader

def generate_short_code(length=6):
    """Generate a short random alphanumeric code for the voucher."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@group_required("Pet Owners")
def generate_single_voucher(request, business_id, discount_type):
    """Generate a single voucher as a PDF and store it on Cloudinary."""

    print("Starting voucher generation...")

    # Get the business and user
    business = get_object_or_404(PetBusiness, id=business_id)
    user = request.user  

    # Check if the voucher already exists
    voucher, created = Voucher.objects.get_or_create(
        user=user,
        pet_business=business,
        discount_type=discount_type,
        defaults={
            'discount_value': 50.00 if discount_type == 'percentage' else 20.00,
            'date_expires': now() + timedelta(days=90),
        }
    )

    # If voucher already exists, redirect to stored Cloudinary URL
    if not created and voucher.pdf_file:
        print(f"Existing voucher found: {voucher.pdf_file}")
        return redirect(voucher.pdf_file)

    print("Creating new voucher...")

    # Ensure voucher has a unique short code
    if not voucher.code:
        voucher.code = generate_short_code()
        voucher.save()

    pdf_filename = f"vouchers/{voucher.code}.pdf"
    print(f"Generated PDF filename: {pdf_filename}")

    # Render HTML for the PDF
    print("Rendering voucher HTML...")
    html_string = render_to_string('vouchers/voucher_pdf.html', {'vouchers': [voucher]})

    if not html_string.strip():
        print("PDF generation failed: Empty HTML template.")
        return HttpResponse("PDF generation failed: Empty HTML template.", status=500)

    print("HTML rendering successful!")

    # Generate the PDF
    pdf_buffer = io.BytesIO()
    try:
        print("Generating PDF with WeasyPrint...")
        HTML(string=html_string).write_pdf(pdf_buffer)
    except Exception as e:
        print(f"PDF generation failed: {e}")
        return HttpResponse(f"PDF generation failed: {str(e)}", status=500)

    # Check if the PDF is empty
    pdf_buffer.seek(0)
    pdf_size = pdf_buffer.getbuffer().nbytes
    print(f"PDF size: {pdf_size} bytes")

    if pdf_size == 0:
        print("PDF generation failed: Empty file.")
        return HttpResponse("PDF generation failed: Empty file.", status=500)

    # Upload the PDF to Cloudinary
    try:
        print("Uploading PDF to Cloudinary...")

        cloudinary_response = cloudinary.uploader.upload(
            pdf_buffer.getvalue(),
            resource_type="raw",
            folder="vouchers/",
            public_id=voucher.code,
            format="pdf"
        )

        # Debugging Cloudinary Response
        print(f"Cloudinary response: {cloudinary_response}")

        # Store the correct Cloudinary URL
        voucher.pdf_file = cloudinary_response.get('secure_url')

        if not voucher.pdf_file:
            return HttpResponse("Error: Cloudinary did not return a valid URL.", status=500)

        voucher.save(update_fields=['pdf_file'])
        print(f"Stored Cloudinary URL: {voucher.pdf_file}")

    except Exception as e:
        error_message = f"Error saving PDF to Cloudinary: {str(e)}"
        print(error_message)  # Logs the error
        return HttpResponse(error_message, status=500)

    return redirect(voucher.pdf_file)
