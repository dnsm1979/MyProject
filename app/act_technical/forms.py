from django.utils import timezone
from django import forms

from cards.models import CardHardware, CardLPU
from .models import ActT

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

    class Meta:
        model = ActT
        fields = ('device', 'lpu', 'user', 'check_result', 
                 'probable_cause', 'conclusion', 'comments', 'location')

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
        
        # Генерация имени акта
        if not instance.name and instance.device:
            date_str = instance.creation_date.strftime("%d%m%Y") if instance.creation_date \
                      else timezone.now().strftime("%d%m%Y")
            instance.name = f"АктТ_{instance.device.serial_number}_{date_str}"
        
        # Установка создателя
        if hasattr(self, 'request') and self.request and not instance.user:
            instance.user = self.request.user
        
        if commit:
            instance.save()
        return instance


class ActEditForm(forms.ModelForm):
    class Meta:
        model = ActT
        fields = '__all__'  # Или укажите конкретные поля
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Если есть экземпляр (редактирование)
        if self.instance and self.instance.pk:
            # Устанавливаем начальные queryset'ы
            self.fields['lpu'].queryset = CardLPU.objects.filter(
                organization=user.organization
            )
            
            # Если есть выбранное ЛПУ, фильтруем оборудование
            if self.instance.lpu:
                self.fields['device'].queryset = CardHardware.objects.filter(
                    lpu=self.instance.lpu
                )
            else:
                self.fields['device'].queryset = CardHardware.objects.none()


# from django import forms

# from .models import ActT



# class ActAddForm(forms.ModelForm):

#     class Meta:
#         model = ActT
#         fields = ('device', 'lpu', 'check_result', 'probable_ause', 'conclusion', 'comments', 'location')

