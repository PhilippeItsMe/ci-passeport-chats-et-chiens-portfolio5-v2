from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
import io
from pet_businesses.utils import group_required

@group_required("Pet Owners")
def generate_vouchers(request, business_id):
    """Generate both vouchers as PDFs from an HTML template."""
    from .models import Voucher
    from pet_businesses.models import PetBusiness
    from pet_owners.models import PetOwner

    business = get_object_or_404(PetBusiness, id=business_id)
    owner = get_object_or_404(PetOwner, author=request.user)

    existing_vouchers = Voucher.objects.filter(pet_owner=owner, pet_business=business)
    if existing_vouchers.count() >= 2:
        return redirect('vouchers:voucher_list')

    vouchers = Voucher.create_vouchers_for_business(business, owner)
    html_string = render_to_string('vouchers/voucher_pdf.html', {'vouchers': vouchers})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="vouchers_{business.id}.pdf"'
    HTML(string=html_string).write_pdf(response)

    for voucher in vouchers:
        individual_html = render_to_string('vouchers/voucher_pdf.html', {'vouchers': [voucher]})
        individual_buffer = io.BytesIO()
        HTML(string=individual_html).write_pdf(individual_buffer)
        voucher.pdf_file.save(f"voucher_{voucher.code}.pdf", ContentFile(individual_buffer.getvalue()))
        voucher.save()
        individual_buffer.close()

    return response

@group_required("Pet Owners")
def generate_single_voucher(request, business_id, discount_type):
    """Generate a single voucher (50% or 20 CHF) as a PDF from an HTML template."""
    from .models import Voucher
    from pet_businesses.models import PetBusiness
    from pet_owners.models import PetOwner

    business = get_object_or_404(PetBusiness, id=business_id)
    owner = get_object_or_404(PetOwner, author=request.user)

    # Check if the voucher for this discount type already exists
    existing_voucher = Voucher.objects.filter(
        pet_owner=owner,
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
    if discount_type == 'percentage':
        voucher = Voucher(
            pet_business=business,
            pet_owner=owner,
            discount_type='percentage',
            discount_value=50.00,
            date_expires=models.DateTimeField.now() + timedelta(days=90)
        )
    elif discount_type == 'fixed':
        voucher = Voucher(
            pet_business=business,
            pet_owner=owner,
            discount_type='fixed',
            discount_value=20.00,
            date_expires=models.DateTimeField.now() + timedelta(days=90)
        )
    else:
        return HttpResponse("Invalid discount type.", status=400)

    voucher.save()  # This triggers code generation via the save method

    # Generate and save the PDF
    html_string = render_to_string('vouchers/voucher_pdf.html', {'vouchers': [voucher]})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="voucher_{voucher.code}.pdf"'
    HTML(string=html_string).write_pdf(response)

    # Save the PDF to the voucher
    individual_buffer = io.BytesIO()
    HTML(string=html_string).write_pdf(individual_buffer)
    voucher.pdf_file.save(f"voucher_{voucher.code}.pdf", ContentFile(individual_buffer.getvalue()))
    voucher.save()
    individual_buffer.close()

    return response

@group_required("Pet Owners")
def voucher_list(request):
    """List all vouchers for the authenticated user."""
    from .models import Voucher
    vouchers = Voucher.objects.filter(pet_owner__author=request.user)
    return render(request, 'vouchers/voucher_list.html', {'vouchers': vouchers})

@group_required("Pet Owners")
def voucher_detail(request, voucher_id):
    """Show details of a specific voucher."""
    from .models import Voucher
    voucher = get_object_or_404(Voucher, id=voucher_id, pet_owner__author=request.user)
    return render(request, 'vouchers/voucher_detail.html', {
        'voucher': voucher,
        'details': voucher.get_full_details()
    })

@group_required("Pet Owners")
def download_voucher_pdf(request, voucher_id):
    """Download the stored PDF for a specific voucher."""
    from .models import Voucher
    voucher = get_object_or_404(Voucher, id=voucher_id, pet_owner__author=request.user)
    if voucher.pdf_file:
        response = HttpResponse(voucher.pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="voucher_{voucher.code}.pdf"'
        return response
    return HttpResponse("PDF not available.", status=404)