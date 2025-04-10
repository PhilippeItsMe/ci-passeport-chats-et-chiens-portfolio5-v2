from django import forms
from .models import PetOwner, Pet
from django.forms.widgets import ClearableFileInput


class PetOwnerForm(forms.ModelForm):
    """
    Form for creating and updating PetOwner instances.
    """
    class Meta:
        model = PetOwner
        fields = [
            'default_street',
            'default_postal_code',
            'default_city',
            'default_country',
            'default_phone',
            'default_newsletter',
        ]
        widgets = {
            'default_street': forms.TextInput(attrs={'class': 'form-control'}),
            'default_postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'default_city': forms.TextInput(attrs={'class': 'form-control'}),
            'default_country': forms.TextInput(attrs={'class': 'form-control'}),
            'default_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'default_newsletter': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'default_street': 'Rue',
            'default_street_number': 'Numéro',
            'default_postal_code': 'Code postal',
            'default_city': 'Ville',
            'default_country': 'Pays',
            'default_phone': 'Vous pouvez sans autre me contacter à ce numéro : ',
            'default_newsletter': 'Je souhaite recevoir votre newsletter.',
        }

class CustomClearableFileInput(ClearableFileInput):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.template_with_initial = '%(input)s'
        self.initial_text = ''
        self.template_with_clear = ''


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
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'
            ),
            'pet_type': forms.Select(attrs={'class': 'form-control'}),
            'pet_featured_image': CustomClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Quel est le nom de votre animal ?',
            'birthday': 'Quel est sa date de naissance ?',
            'pet_type': 'Quel est son type d’animal ? ',
            'pet_featured_image': "Une image à partager de votre compagnon ?",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.birthday:
            self.initial['birthday'] = self.instance.birthday.strftime('%Y-%m-%d')