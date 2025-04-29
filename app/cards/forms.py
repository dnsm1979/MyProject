import re
from django import forms

from main.models import City
from cards.models import CardLPU, CardHardware



class AddLPUForm(forms.ModelForm):

    class Meta:
        model = CardLPU
        fields = ('name', 'adress', 'index', 'zip','representative_1', 'representative_2', 'representative_3', 'phone', 'city')

    # name = forms.CharField()
    # adress = forms.CharField(widget=forms.Textarea)
    # index = forms.CharField()
    # zip  = forms.CharField()
    # representative_1 = forms.CharField()
    # representative_2 = forms.CharField()
    # representative_3 = forms.CharField()
    # phone = forms.CharField()
    # city = forms.ModelChoiceField(
    #                             queryset = City.objects.all(), to_field_name="city")

    # def clean_phone(self):
    #     data = self.cleaned_data['phone']

    #     if not data.isdigit():
    #         raise forms.ValidationError("Номер телефона должен содержать только цифры")
        
    #     pattern = re.compile(r'^\d{10}$')
    #     if not pattern.match(data):
    #         raise forms.ValidationError("Неверный формат номера")

    #     return data


class AddHardwareForm(forms.ModelForm):

    class Meta:
        model = CardHardware
        fields = ('__all__')


    # name = forms.CharField()
    # model = forms.CharField()
    # serial_number = forms.CharField()
    # invent_number = forms.CharField()
    # year_of_manufacture = forms.CharField()
    # year_of_sale = forms.CharField()
    # commissioning_date = forms.CharField()
    # lpu = forms.ModelChoiceField(required = True, 
    #                             label = "CardLPU",
    #                             queryset = CardLPU.objects.all(),
    #                             widget = forms.Select(attrs = {
    #                                 "class": "form-list-field"}
    #                             ))
    # cauntry = forms.CharField()
    # manufacturer = forms.CharField()