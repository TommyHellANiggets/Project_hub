from .models import Fuel, Review
from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Искать на Power Fuel…'}))

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'content']

class FuelForm(forms.ModelForm):
    class Meta:
        model = Fuel
        fields = ['name', 'description', 'price', 'photo_url']