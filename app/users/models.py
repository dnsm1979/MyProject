from django.db import models
from django.contrib.auth.models import AbstractUser

class UserCategory(models.Model):
    profcategory = models.CharField(
    max_length=150,
    blank=True,
    null=True,
    unique=False,
    verbose_name='Проф-категория',
    default=None
)
    class Meta:
        db_table = 'usercategory'
        verbose_name = 'Проф-категория'
        verbose_name_plural = 'Проф-категории'

    def __str__(self):
        return self.profcategory

class User(AbstractUser):
    position = models.CharField(
    max_length=150,
    blank=True,
    null=True,
    unique=False,
    verbose_name='Должность',
    default=None
)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    surname  = models.CharField(max_length=150, unique=True, verbose_name='Отчество')
    profcategory = models.ForeignKey('UserCategory', on_delete=models.SET_NULL, blank=True, null=True,  related_name='usercategory')

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
    
