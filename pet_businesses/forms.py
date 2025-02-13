from django import forms
from .models import PetBusiness, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class PetBusinessForm(forms.ModelForm):
    """
    Form for creating and updating PetBusiness instances.
    """
    class Meta:
        model = PetBusiness
        fields = [
            'firm',
            'slug',
            'street',
            'number',
            'npa',
            'locality',
            'phone',
            'email',
            'website',
            'featured_image',
            'linkedin',
            'facebook',
            'instagram',
            'tiktok',
            'business_pet_type',
            'business_service_type',
            'description',
        ]
        widgets = {
            'firm': forms.TextInput(attrs={'class': 'form-control',
                                           'id': 'firm-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-control',
                                           'id': 'slug-input'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'npa': forms.TextInput(attrs={'class': 'form-control'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'featured_image': forms.ClearableFileInput(attrs={'class':
                                                              'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control'}),
            'tiktok': forms.URLInput(attrs={'class': 'form-control'}),
            'business_pet_type': forms.CheckboxSelectMultiple(),
            'business_service_type': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'firm': 'Votre entreprise ',
            'slug': 'Url de votre page (remplie automatiquement) ',
            'street': 'Rue ',
            'number': 'N° ',
            'npa': 'Code postale ',
            'locality': 'Localité ',
            'phone': 'Téléphone ',
            'email': 'Email ',
            'website': 'Website (https://...) ',
            'featured_image': "Illustration ",
            'linkedin': 'Page LinkedIn (https://...) ',
            'facebook': 'Page Facebook (https://...) ',
            'instagram': 'Page Instagram (https://...) ',
            'tiktok': 'Page TikTok (https://...) ',
            'business_pet_type': 'Animaux servis ',
            'business_service_type': 'Types de services offerts ',
            'description': 'Description ',
        }


class CommentForm(forms.ModelForm):
    """
    Form to enter comments.
    """
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'id': 'id_body'}),
        }
        labels = {
            'content': 'Contenu'
        }


class UserRegistrationForm(UserCreationForm):
    """
    User registration form extending Django's built-in UserCreationForm.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomSignupForm(forms.Form):
    """
    Custom signup form to register users by group, first name, and last name.
    """
    group_choices = [
        ('Pet Owners', 'Propriétaire d\'un animal'),
        ('Business Owners', 'Propriétaire d\'un service animalier'),
    ]
    group = forms.ChoiceField(choices=group_choices,
                              label="Je m'enregiste en tant que : ")
    
    first_name = forms.CharField(max_length=30, label='Prénom', required=True)
    last_name = forms.CharField(max_length=30, label='Nom', required=True)

    field_order = ['first_name', 'last_name', 'group','email','email2',
                    'password1', 'password2']

    def signup(self, request, user):

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        group_name = self.cleaned_data['group']
        try:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        except Group.DoesNotExist:
            raise ValueError(f"Le groupe '{group_name}' n'existe pas.")
        user.save()
        return user
