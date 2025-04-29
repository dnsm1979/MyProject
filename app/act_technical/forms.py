from django import forms

from cards.models import CardLPU, CardHardware



class ActAddForm(forms.Form):

    
    creation_date = forms.DateField()
    representative_1 = forms.CharField()
    representative_2 = forms.CharField()
    representative_3 = forms.CharField()
    lpu = forms.ModelChoiceField(required = True, 
                                label = "CardLPU",
                                queryset = CardLPU.objects.all(),
                                widget = forms.Select(attrs = {
                                    "class": "form-list-field"}
                                ))
    device = forms.ModelChoiceField(required = True, 
                                label = "CardHardware",
                                queryset = CardHardware.objects.all(),
                                widget = forms.Select(attrs = {
                                    "class": "form-list-field"}
                                ))
    check_result = forms.CharField(widget=forms.Textarea)
    probable_ause = forms.CharField(widget=forms.Textarea)
    conclusion  = forms.CharField(widget=forms.Textarea)
