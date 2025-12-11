from django import forms
from .models import Recharge

class RechargeForm(forms.ModelForm):
    terms = forms.BooleanField(
        required=True,
        label="J'accepte les termes et conditions"
    )

    class Meta:
        model = Recharge
        fields = [
            'first_name',
            'last_name',
            'phone',
            'email',
            'recharge_code',
            'recharge_type',
            'expiration_date',
            'terms'
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Prénom',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nom',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+33 6 12 34 56 78',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'votre@email.com',
                'required': True
            }),
            'recharge_code': forms.PasswordInput(attrs={
                'class': 'form-input',
                'placeholder': 'Entrez votre code',
                'required': True,
                'id': 'rechargeCode'
            }),
            'recharge_type': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }, choices=[
                ('', 'Veuillez sélectionner'),
                ('transcash', 'Transcash'),
                ('pcs', 'PCS Mastercard'),
                ('neosurf', 'Néosurf'),
                ('steam', 'Steam'),
                ('google_play', 'Google Play'),
                ('itunes', 'iTunes'),
                ('paysafecard', 'Paysafecard'),
                ('amazon', 'Amazon'),
            ]),
            'expiration_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
                'required': True
            }),
        }

    def clean_terms(self):
        terms = self.cleaned_data.get('terms')
        if not terms:
            raise forms.ValidationError("Vous devez accepter les termes et conditions.")
        return terms
