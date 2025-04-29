
from django import forms

from cards.models import CardLPU, CardHardware



class AddLPUForm(forms.ModelForm):

    class Meta:
        model = CardLPU
        fields = ('__all__')



class AddHardwareForm(forms.ModelForm):

    

    class Meta:
        model = CardHardware
        fields = ('__all__')


    def __init__(self, *args, **kwargs):
        lpu_id = kwargs.pop('lpu_id', None)
        super().__init__(*args, **kwargs)
        
        if lpu_id:
            self.fields['lpu'].initial = lpu_id

