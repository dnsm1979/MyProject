from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    position  = models.CharField(max_length=150, unique=True, verbose_name='Должность')
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    surname  = models.CharField(max_length=150, unique=True, verbose_name='Отчество')

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username