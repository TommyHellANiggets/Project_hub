from .models import Fuel, Review
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'content']

class FuelForm(forms.ModelForm):
    class Meta:
        model = Fuel
        fields = ['name', 'description', 'price', 'photo_url']
