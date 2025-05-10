from django.utils import timezone
from django import forms
from django.forms import ClearableFileInput
from cards.models import CardHardware, CardLPU
from .models import ActT
from .models import ActImage
from django.forms import widgets
from django.core.exceptions import ValidationError
from django.forms import Field

class ActAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Достаем request из kwargs перед вызовом родительского __init__
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # Настройка виджетов
        textarea_fields = ['check_result', 'probable_cause', 'conclusion', 'comments']
        for field in textarea_fields:
            self.fields[field].widget = forms.Textarea(attrs={'rows': 3})
        
        # Скрываем технические поля
        # self.fields['name'].widget = forms.HiddenInput()
        # self.fields['user'].widget = forms.HiddenInput()
        
        # Устанавливаем текущего пользователя
        if self.request and not self.instance.pk:
            self.initial['user'] = self.request.user

        if self.instance.pk and not self.initial.get('creation_date'):
            self.initial['creation_date'] = self.instance.creation_date.date()


    class Meta:
        model = ActT
        fields = ('device', 'lpu', 'user', 'check_result', 
                 'probable_cause', 'conclusion', 'comments', 'creation_date', 'location')

    def clean_device(self):
        device = self.cleaned_data.get('device')
        if device and not device.serial_number:
            raise forms.ValidationError(
                "У выбранного оборудования отсутствует серийный номер. "
                "Пожалуйста, укажите серийный номер в карточке оборудования."
            )
        return device

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        
        # Установка создателя
        if hasattr(self, 'request') and self.request and not instance.user:
            instance.user = self.request.user
        
        if commit:
            instance.save()
        return instance




class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]
        return [single_file_clean(data, initial)]

class UploadImagesForm(forms.ModelForm):
    images = MultipleFileField(label='Выберите изображения')

    class Meta:
        model = ActImage
        fields = ['description']