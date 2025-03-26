from django import forms
from .models import PetOwner, Pet


class PetOwnerForm(forms.ModelForm):
    """
    Form for creating and updating PetOwner instances.
    """
    class Meta:
        model = PetOwner
        fields = [
            'street',
            'street_number',
            'postal_code',
            'city',
            'country',
            'phone',
            'newsletter',
        ]
        widgets = {
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'street_number': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'newsletter': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}),
        }
        labels = {
            'street': 'Rue',
            'street_number': 'Numéro',
            'postal_code': 'Code postal',
            'city': 'Ville',
            'country': 'Pays',
            'phone': 'Vous pouvez sans autre me contacter à ce numéro : ',
            'newsletter': 'Je souhaite recevoir votre newsletter.',
        }


class PetForm(forms.ModelForm):
    """
    Form for creating and updating Pet instances.
    """
    class Meta:
        model = Pet
        fields = [
            'name',
            'birthday',
            'pet_type',
            'pet_featured_image',
        ]
        error_messages = {
            'name': {
                'required': 'Veuillez renseigner le nom de votre animal.',
            },
        },
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control',
                                               'type': 'date'}),
            'pet_type': forms.Select(attrs={'class': 'form-control'}),
            'pet_featured_image': forms.ClearableFileInput(
                attrs={'class':'form-control'}),
        }
        labels = {
            'name': 'Nom de votre animal ',
            'birthday': 'Sa date de naissance ',
            'pet_type': 'Type d’animal ',
            'pet_featured_image': "Image de l'animal ",
        }