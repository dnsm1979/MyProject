from django.db import models
from django.urls import reverse
from users.models import User

class Country(models.Model):
    country = models.CharField(max_length=150, unique=True, verbose_name='Страна')

    class Meta:
        db_table = 'country'
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ("id",)

    def __str__(self):
        return self.country
    
class City(models.Model):
    city = models.CharField(max_length=200, unique=True, verbose_name='Город')

    class Meta:
        db_table = 'city'
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ("id",)

    def __str__(self):
        return self.city
    


class Region(models.Model):
    zip = models.CharField(max_length=200, unique=True, verbose_name='Регион')

    class Meta:
        db_table = 'zip'
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
        ordering = ("id",)

    def __str__(self):
        return f"{self.zip}"
    

class Templates(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название")
    text = models.TextField(null=True, blank=True, verbose_name='Текст шаблона')
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Пользователь", default=None)

    class Meta:
        db_table = 'templates'
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'
        ordering = ("id",)

    def __str__(self):
        return self.name