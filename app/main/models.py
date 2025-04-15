from django.db import models
from django.urls import reverse
from users.models import User

class Info(models.Model):
    country = models.CharField(max_length=150, unique=True, verbose_name='Страна')
    city = models.CharField(max_length=200, unique=True, blank=True, null=True, verbose_name='Город')

    class Meta:
        db_table = 'info'
        verbose_name = 'Информацию'
        verbose_name_plural = 'Информация'
        ordering = ("id",)

    def __str__(self):
        return self.id
    

class Templates(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название")
    text = models.TextField(null=True, blank=True, verbose_name='Текст шаблона')
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, blank=True, null=True, verbose_name="Пользователь", default=None)

    class Meta:
        db_table = 'templates'
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'
        ordering = ("id",)

    def __str__(self):
        return self.name