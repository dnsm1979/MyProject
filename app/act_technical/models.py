from django.db import models
from image_manager.models import Location
from cards.models import CartLPU, CartHardware
from users.models import User


class ActT(models.Model):

    name = models.CharField(max_length=150, verbose_name="Название")
    lpu = models.ForeignKey(to=CartLPU, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Владелец")
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Пользователь", default=None)
    device = models.ForeignKey(to=CartHardware, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Оборудование")
    check_result = models.TextField(null=True, blank=True, verbose_name="Результат проверки")
    probable_ause = models.TextField(null=True, blank=True, verbose_name="Вероятная причина")
    conclusion = models.TextField(null=True, blank=True, verbose_name="Заключение")
    comments = models.TextField(null=True, blank=True, verbose_name="Коментарии")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    location = models.ForeignKey(Location, related_name="location", on_delete=models.SET_NULL, blank=True, null=True)



    class Meta:
        db_table = 'actt'
        verbose_name = "Акт техсостояния"
        verbose_name_plural = "Акты техсостояния"
        ordering = ("id",)

    def __str__(self):
        return self.name

