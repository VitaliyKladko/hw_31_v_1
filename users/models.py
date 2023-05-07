from django.db import models
from django.db.models import TextChoices


class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        verbose_name = 'Местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class UserRoles(TextChoices):
    MEMBER = 'member', 'Пользователь'
    ADMIN = 'admin', 'Админ'
    MODERATOR = 'moderator', 'Модератор'


class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    age = models.PositiveSmallIntegerField()
    locations = models.ManyToManyField(Location)
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
