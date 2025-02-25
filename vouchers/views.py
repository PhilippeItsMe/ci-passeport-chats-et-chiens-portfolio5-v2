from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from weasyprint import HTML  # To convert HTML to PDF
from django.template.loader import render_to_string  # To render the HTML template as a string
from django.core.files.base import ContentFile
import io
from pet_businesses.utils import group_required

@group_required("Pet Owners")
def generate_vouchers(request, business_id):
    """Generate vouchers as PDFs from an HTML template."""
    # Lazy imports to avoid circular import issues
    from .models import Voucher
    from pet_businesses.models import PetBusiness
    from pet_owners.models import PetOwner

    # Retrieve the necessary objects
    business = get_object_or_404(PetBusiness, id=business_id)
    owner = get_object_or_404(PetOwner, author=request.user)

    # Check if vouchers already exist
    existing_vouchers = Voucher.objects.filter(pet_owner=owner, pet_business=business)
    if existing_vouchers.count() >= 2:
        return redirect('vouchers:voucher_list')  # Redirect if vouchers already exist

    # Generate the vouchers
    vouchers = Voucher.create_vouchers_for_business(business, owner)

    # Render the HTML template as a string for the combined PDF
    html_string = render_to_string('vouchers/voucher_pdf.html', {'vouchers': vouchers})

    # Prepare the HTTP response for downloading the combined PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="vouchers_{business.id}.pdf"'
    
    # Convert the HTML to PDF and write it to the response
    HTML(string=html_string).write_pdf(response)

    # Save individual PDFs for each voucher
    for voucher in vouchers:
        individual_html = render_to_string('vouchers/voucher_pdf.html', {'vouchers': [voucher]})
        individual_buffer = io.BytesIO()
        HTML(string=individual_html).write_pdf(individual_buffer)
        voucher.pdf_file.save(f"voucher_{voucher.code}.pdf", ContentFile(individual_buffer.getvalue()))
        voucher.save()
        individual_buffer.close()

    return response

@group_required("Pet Owners")
def voucher_list(request):
    """List all vouchers for the authenticated user."""
    from .models import Voucher  # Lazy import
    vouchers = Voucher.objects.filter(pet_owner__author=request.user)
    return render(request, 'vouchers/voucher_list.html', {'vouchers': vouchers})

@group_required("Pet Owners")
def voucher_detail(request, voucher_id):
    """Show details of a specific voucher."""
    from .models import Voucher  # Lazy import
    voucher = get_object_or_404(Voucher, id=voucher_id, pet_owner__author=request.user)
    return render(request, 'vouchers/voucher_detail.html', {
        'voucher': voucher,
        'details': voucher.get_full_details()
    })

@group_required("Pet Owners")
def download_voucher_pdf(request, voucher_id):
    """Download the stored PDF for a specific voucher."""
    from .models import Voucher  # Lazy import
    voucher = get_object_or_404(Voucher, id=voucher_id, pet_owner__author=request.user)
    if voucher.pdf_file:
        response = HttpResponse(voucher.pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="voucher_{voucher.code}.pdf"'
        return response
    return HttpResponse("PDF not available.", status=404)
