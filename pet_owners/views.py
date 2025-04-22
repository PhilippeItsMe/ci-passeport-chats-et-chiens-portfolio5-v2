from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import PetOwner, Pet
from .forms import PetOwnerForm, PetForm
from pet_businesses.utils import group_required


@group_required("Pet Owners")
def pet_owner_form(request):
    """
    View to create or update pet owner details
    """
    try:
        pet_owner = PetOwner.objects.get(author=request.user)
    except PetOwner.DoesNotExist:
        pet_owner = None

    if request.method == "POST":
        form = PetOwnerForm(request.POST, instance=pet_owner)
        if form.is_valid():
            pet_owner = form.save(commit=False)
            pet_owner.author = request.user
            pet_owner.save()
            messages.success(request, "Vos informations ont été mises à jour.")
            return redirect('pet_owner_form')
        else:
            messages.error(request, "Il y a eu une erreur.")
    else:
        form = PetOwnerForm(instance=pet_owner)

    return render(request, 'pet_owners/pet_owners_form.html',
                  {'form': form, 'pet_owner': pet_owner})


@group_required("Pet Owners")
def pet_list(request):
    """
    View to list all pets of the logged-in user (author).
    """
    pets = Pet.objects.filter(author=request.user)

    return render(request, 'pet_owners/pet_owners_pets.html', {
        'pets': pets
    })


@group_required("Pet Owners")
def pet_create(request):
    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.author = request.user  # Linking pet to the current user
            pet.save()
            messages.success(request, f"L'animal {pet.name} a été ajouté avec succès.")
            return redirect('pet_list')
        else:
            messages.error(request, "Il y a eu une erreur.")
    else:
        form = PetForm()

    return render(request, 'pet_owners/pet_form.html', {
        'form': form,
    })



@group_required("Pet Owners")
def pet_edit(request, pet_id):
    """
    View to update a pet
    """
    pet = get_object_or_404(Pet, id=pet_id, author=request.user)

    if request.method == "POST":
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            pet = form.save()
            messages.success(request, f"L'animal {pet.name} a été mis à jour avec succès.")
            return redirect('pet_list')
        else:
            messages.error(request, "Il y a eu une erreur.")
    else:
        form = PetForm(instance=pet)

    return render(request, 'pet_owners/pet_form.html', {
        'form': form,
        'pet': pet,
    })


@group_required("Pet Owners")
def pet_delete(request, pet_id):
    """
    View to delete a pet
    """
    pet = get_object_or_404(Pet, id=pet_id, author=request.user)

    if request.method == "POST":
        pet.delete()
        messages.success(request, f"L'animal {pet.name} a été supprimé avec succès.")
        return redirect('pet_list')
    else:
        messages.error(request, "Il y a eu une erreur.")

    return redirect('pet_list')
