from django.db import models
from main.models import Info




class CartLPU(models.Model):

    name = models.CharField(max_length=250, verbose_name="Название")
    adress = models.TextField(blank=True, null=True, verbose_name="Улица, строение")
    index = models.CharField(max_length=10, verbose_name="Индекс")
    zip  = models.CharField(max_length=250, verbose_name="Область, край")
    representative_1 = models.CharField(max_length=250, blank=True, null=True, verbose_name="Представитель ЛПУ 1")
    representative_2 = models.CharField(max_length=250, blank=True, null=True, verbose_name="Представитель ЛПУ 2")
    representative_3 = models.CharField(max_length=250, blank=True, null=True, verbose_name="Представитель ЛПУ 3")
    lpu = models.CharField(max_length=150, verbose_name="Владелец")
    city = models.ForeignKey(to=Info, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Город")

    class Meta:
        db_table = 'cart_lpu'
        verbose_name = "Организация"
        verbose_name_plural = "Организации"
        ordering = ("id",)

    def __str__(self):
        return self.name

class CartHardware(models.Model):

    name = models.CharField(max_length=150, verbose_name="Название")
    model = models.CharField(max_length=150, verbose_name="Марка")
    serial_number = models.CharField(max_length=150, verbose_name="Серийный номер")
    invent_number = models.CharField(max_length=150, verbose_name="Инвентарный номер")
    year_of_manufacture = models.DateTimeField(verbose_name='Дата производства')
    year_of_sale = models.DateTimeField(verbose_name='Дата продажи')
    commissioning_date = models.DateTimeField(verbose_name='Дата ввода в эксплуатацию')
    lpu = models.ForeignKey(to=CartLPU, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Владелец")
    cauntry = models.ForeignKey(to=Info, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Страна")

    class Meta:
        db_table = 'cart_hardware'
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"
        ordering = ("id",)

    def __str__(self):
        return self.name




