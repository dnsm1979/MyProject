from django.db import models
from main.models import City, Country, Region




class CardLPU(models.Model):

    name = models.CharField(max_length=250, blank=True, null=True, verbose_name="Название")
    adress = models.TextField(blank=True, null=True, verbose_name="Улица, строение")
    index = models.CharField(max_length=10, blank=True, null=True, verbose_name="Индекс")
    zip  = models.ForeignKey(to=Region, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Регион")
    representative_1 = models.CharField(max_length=250, blank=True, null=True, verbose_name="Представитель ЛПУ 1")
    representative_2 = models.CharField(max_length=250, blank=True, null=True, verbose_name="Представитель ЛПУ 2")
    representative_3 = models.CharField(max_length=250, blank=True, null=True, verbose_name="Представитель ЛПУ 3")
    
    city = models.ForeignKey(to=City, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Город")
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="Телефон")

    class Meta:
        db_table = 'card_lpu'
        verbose_name = "Организация"
        verbose_name_plural = "Организации"
        ordering = ("id",)

    def __str__(self):
        return f"{self.name}"

class CardHardware(models.Model):

    name = models.CharField(max_length=150, verbose_name="Название")
    model = models.CharField(max_length=150, verbose_name="Марка")
    serial_number = models.CharField(max_length=150, verbose_name="Серийный номер")
    invent_number = models.CharField(max_length=150,blank=True, null=True, verbose_name="Инвентарный номер")
    year_of_manufacture = models.CharField(max_length=10, verbose_name='Дата производства')
    year_of_sale = models.CharField(max_length=10, verbose_name='Дата продажи')
    commissioning_date = models.CharField(max_length=10, verbose_name='Дата ввода в эксплуатацию')
    lpu = models.ForeignKey(to=CardLPU, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Владелец")
    country = models.ForeignKey(to=Country, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Страна")
    manufacturer = models.CharField(max_length=150, verbose_name="Производитель")

    class Meta:
        db_table = 'card_hardware'
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"
        ordering = ("id",)

    def __str__(self):
        return f"{self.name}"




