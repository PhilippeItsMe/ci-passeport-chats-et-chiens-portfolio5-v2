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
    
    print("Starting voucher generation...")  # Log start

    # Retrieve the business linked to the provided ID
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

    if not created and voucher.pdf_file:
        print("Returning existing voucher PDF.")  # Debug
        return HttpResponse(voucher.pdf_file.url, content_type='application/pdf')

    print("Creating new voucher...")  # Debug

    # Ensure voucher has a code before generating the filename
    if not voucher.code:
        voucher.code = voucher._generate_unique_code()
        voucher.save()

    pdf_filename = f"vouchers/voucher_{voucher.code}.pdf"
    print(f"Generated PDF filename: {pdf_filename}")  # Debug

    # Render the HTML for the PDF
    print("Rendering voucher HTML...")
    html_string = render_to_string('vouchers/voucher_pdf.html', {'vouchers': [voucher]})

    if not html_string.strip():
        print("PDF generation failed: Empty HTML template.")  # Debug
        return HttpResponse("PDF generation failed: Empty HTML template.", status=500)

    print("HTML rendering successful!")  # Debug

    # Generate the PDF
    pdf_buffer = io.BytesIO()
    try:
        print("Generating PDF with WeasyPrint...")
        HTML(string=html_string).write_pdf(pdf_buffer)
    except Exception as e:
        print(f"PDF generation failed: {e}")  # Debug
        return HttpResponse(f"PDF generation failed: {str(e)}", status=500)

    # Check if the PDF is empty
    pdf_buffer.seek(0)
    pdf_size = pdf_buffer.getbuffer().nbytes
    print(f"PDF size: {pdf_size} bytes")  # Debug

    if pdf_size == 0:
        print("PDF generation failed: Empty file.")  # Debug
        return HttpResponse("PDF generation failed: Empty file.", status=500)

    # Save the PDF to Cloudinary
    try:
        print("Saving PDF to Cloudinary...")

        # Ensure the file is correctly uploaded to Cloudinary
        voucher.pdf_file.save(f"{voucher.code}.pdf", ContentFile(pdf_buffer.getvalue()), save=True)
        print(f"PDF saved successfully to Cloudinary: {voucher.pdf_file.url}")  # Debugging

    except Exception as e:
        error_message = f"Error saving PDF to Cloudinary: {str(e)}"
        print(error_message)  # Logs the error
        return HttpResponse(error_message, status=500)


    # Serve the PDF as a response
    pdf_buffer.seek(0)
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
    
    print("Voucher PDF successfully generated and served!")  # Debug
    return response
