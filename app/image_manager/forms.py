from django import forms
from .models import Location, Photo

class LocationForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}), required=False)

    class Meta:
        model = Location
        fields = ['name', 'images']