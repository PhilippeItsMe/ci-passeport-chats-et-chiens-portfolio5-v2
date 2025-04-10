from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 'phone',
            'street',
            'postal_code', 'city', 'country',
        )

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Prénom et nom',
            'email': 'Email',
            'phone': 'Mobile',
            'street': 'Rue et n°',
            'postal_code': 'Code postal',
            'city': 'Localité',
            'country': 'Pays',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            placeholder = placeholders.get(field, '')
            if self.fields[field].required:
                placeholder += ' *'
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
