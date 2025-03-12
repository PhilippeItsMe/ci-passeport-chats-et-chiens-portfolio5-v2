import io
import hashlib
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

@group_required("Pet Owners")
def generate_single_voucher(request, business_id, discount_type):
    """Generate a single voucher as a PDF and store it on Cloudinary."""
    business = get_object_or_404(PetBusiness, id=business_id)
    user = request.user  

    # Create or fetch existing voucher
    voucher, created = Voucher.objects.get_or_create(
        user=user, pet_business=business, discount_type=discount_type,
        defaults={'discount_value': 50.00 if discount_type == 'percentage' else 20.00,
                  'date_expires': now() + timedelta(days=90)}
    )

    # Redirect if PDF already exists
    if not created and voucher.pdf_file:
        return redirect(voucher.pdf_file.url if hasattr(voucher.pdf_file, 'url') else voucher.pdf_file)

    # Ensure voucher has a unique code
    if not voucher.code:
        voucher.code = voucher._generate_unique_code()
        voucher.save()

    # Shorten the filename using a hash
    short_code = hashlib.md5(voucher.code.encode()).hexdigest()[:8]
    pdf_filename = f"v_{short_code}.pdf"

    # Render voucher HTML
    html_string = render_to_string('vouchers/voucher_pdf.html', {'vouchers': [voucher]})
    if not html_string.strip():
        return HttpResponse("PDF generation failed: Empty HTML template.", status=500)

    # Generate PDF
    pdf_buffer = io.BytesIO()
    try:
        HTML(string=html_string).write_pdf(pdf_buffer)
    except Exception as e:
        return HttpResponse(f"PDF generation failed: {str(e)}", status=500)

    # Ensure PDF is not empty
    pdf_buffer.seek(0)
    if pdf_buffer.getbuffer().nbytes == 0:
        return HttpResponse("PDF generation failed: Empty file.", status=500)

    # Upload PDF directly to Cloudinary
    try:
        cloudinary_response = cloudinary.uploader.upload(
            pdf_buffer.getvalue(), resource_type="raw", folder="vouchers/",
            public_id=f"v_{short_code}", format="pdf"
        )
        voucher.pdf_file = cloudinary_response.get('secure_url', cloudinary_response.get('url'))
        voucher.save(update_fields=['pdf_file'])

    except Exception as e:
        return HttpResponse(f"Error saving PDF to Cloudinary: {str(e)}", status=500)

    #return redirect(voucher.pdf_file)
    #return redirect(f"{voucher.pdf_file}.pdf")
    #return redirect(voucher.pdf_file.replace("/upload/", "/upload/fl_attachment:pdf/"))

    #pdf_url = voucher.pdf_file.replace("/upload/", "/upload/resource_type:raw/")
    #return redirect(pdf_url)

    pdf_url = f"{voucher.pdf_file}?dl=voucher.pdf"
    print(f"Final Redirect URL: {pdf_url}")
    return redirect(pdf_url)
