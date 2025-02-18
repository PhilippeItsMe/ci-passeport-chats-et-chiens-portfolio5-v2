from django import forms
from .models import PetOwner, Pet


class PetOwnerForm(forms.ModelForm):
    """
    Form for creating and updating PetOwner instances.
    """
    class Meta:
        model = PetOwner
        fields = [
            'phone',
            'newsletter',
        ]
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'newsletter': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'phone': 'Vous pouvez sans autre me contacter à ce numéro si nécessaire : ',
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