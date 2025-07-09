from django import forms
from .models import SpecialOffer

class SpecialOfferForm(forms.ModelForm):
    class Meta:
        model = SpecialOffer
        fields = ['title', 'description', 'image']