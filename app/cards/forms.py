from django import forms



class AddLPUForm(forms.Form):

    
    name = forms.CharField()
    adress = forms.CharField(widget=forms.Textarea)
    index = forms.CharField()
    zip  = forms.CharField()
    representative_1 = forms.CharField()
    representative_2 = forms.CharField()
    representative_3 = forms.CharField()
    lpu = forms.CharField()
    city = forms.CharField()


class AddHardwareForm(forms.Form):


    name = forms.CharField()
    model = forms.CharField()
    serial_number = forms.CharField()
    invent_number = forms.CharField()
    year_of_manufacture = forms.CharField()
    year_of_sale = forms.CharField()
    commissioning_date = forms.CharField()
    lpu = forms.CharField()
    cauntry = forms.CharField()
    manufacturer = forms.CharField()