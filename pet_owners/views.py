from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Pet, PetOwner
from .forms import PetOwnerForm, PetForm
from pet_businesses.utils import group_required
from django.core.exceptions import PermissionDenied


@group_required("Pet Owners")
def pet_owner_form(request):

    """
    View to render pet owner personal info.
    """
    pet_owner = PetOwner.objects.filter(
        author=request.user, approved=True)

    if request.method == "POST":
        form = PetOwnerForm(request.POST)

        if form.is_valid():
            pet_business = form.save(commit=False)
            pet_business.author = request.user
            pet_business.save()
            form.save_m2m()
            messages.success(request,
                             "Changement en attente d'approbation.")
            return redirect('pet_owner_form')
        else:
            messages.error(request, "Il y a eu une erreur.")
    else:
        form = PetOwnerForm()

    return render(request, 'pet_businesses/pet_business_form.html', {
        'pet_owners': pet_owner, 'form': form,
    })



