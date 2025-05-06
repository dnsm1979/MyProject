from django.utils import timezone
from django.db import models
from image_manager.models import Location
from cards.models import CardLPU, CardHardware
from users.models import User


class ActT(models.Model):

    name = models.CharField(max_length=150, verbose_name="Название")
    lpu = models.ForeignKey(to=CardLPU, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Владелец")
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Пользователь", default=None)
    device = models.ForeignKey(to=CardHardware, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Оборудование")
    check_result = models.TextField(null=True, blank=True, verbose_name="Результат проверки")
    probable_cause = models.TextField(null=True, blank=True, verbose_name="Вероятная причина")
    conclusion = models.TextField(null=True, blank=True, verbose_name="Заключение")
    comments = models.TextField(null=True, blank=True, verbose_name="Коментарии")
    creation_date = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    location = models.ForeignKey(Location, related_name="location", on_delete=models.SET_NULL, blank=True, null=True)


    def save(self, *args, **kwargs):
        # Устанавливаем создателя только при первом сохранении
        if not self.pk and not self.name:
            request = kwargs.pop('request', None)
            if request and hasattr(request, 'user'):
                self.name = request.user
        
        # Сначала сохраняем, чтобы получить ID
        if not self.pk:
            super().save(*args, **kwargs)
        
        # Генерируем название после сохранения
        self.generate_act_name()
        
        # Сохраняем с обновлённым названием
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'actt'
        verbose_name = "Акт техсостояния"
        verbose_name_plural = "Акты техсостояния"
        ordering = ("-creation_date",)

    def generate_act_name(self):
        date_str = self.creation_date.strftime("%d%m%Y") if self.creation_date \
            else timezone.now().strftime("%d%m%Y")
        self.name = f"АктТ_{self.id}_{date_str}"


    def __str__(self):
        return self.name if self.name else f"АктТ_{self.id or 'новый'}"
    

