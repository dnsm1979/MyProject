from datetime import timezone
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
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    location = models.ForeignKey(Location, related_name="location", on_delete=models.SET_NULL, blank=True, null=True)


    def save(self, *args, **kwargs):
        # Устанавливаем создателя только при первом сохранении
        if not self.pk and not self.name:
            request = kwargs.pop('request', None)
            if request and hasattr(request, 'user'):
                self.name = request.user
        
        # Генерируем имя акта если оно не задано и есть привязанное оборудование
        if not self.name and self.device:
            try:
                date_str = timezone.now().strftime("%d%m%Y")
                self.name = f"АктТ_{self.device.serial_number}_{date_str}"
            except AttributeError:
                # На случай если у оборудования нет serial_number
                self.name = f"АктТ_{timezone.now().strftime('%d%m%Y_%H%M%S')}"
        
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'actt'
        verbose_name = "Акт техсостояния"
        verbose_name_plural = "Акты техсостояния"
        ordering = ("-creation_date",)

    def __str__(self):
        return self.name or f"АктТ #{self.id}"
    

    # def save(self, *args, **kwargs):
    #     if not self.pk:  # Только при создании нового объекта
    #         self.created_by = kwargs.pop('user', None) or (hasattr(self, '_request_user') and self._request_user)
    #     super().save(*args, **kwargs)

    #     if not self.name and self.device_id:
    #         device = CardHardware.objects.get(pk=self.device_id)
    #         date_str = timezone.now().strftime("%d%m%Y")
    #         self.name = f"АктТ_{device.serial_number}_{date_str}"
    #     super().save(*args, **kwargs)



    # class Meta:
    #     db_table = 'actt'
    #     verbose_name = "Акт техсостояния"
    #     verbose_name_plural = "Акты техсостояния"
    #     ordering = ("id",)

    # def __str__(self):
    #     return self.name

