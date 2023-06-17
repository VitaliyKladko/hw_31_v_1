from django.core.validators import RegexValidator
from django.db import models
from django.db.models import TextChoices
from django.contrib.auth.models import AbstractUser

from users.validators import check_age


class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    class Meta:
        verbose_name = 'Местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class UserRoles(TextChoices):
    MEMBER = 'member', 'Пользователь'
    ADMIN = 'admin', 'Админ'
    MODERATOR = 'moderator', 'Модератор'


class User(AbstractUser):
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    locations = models.ManyToManyField(Location)
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)
    birth_date = models.DateField(null=True, blank=True, validators=[check_age])
    email = models.EmailField(validators=[RegexValidator(
        regex='@rambler.ru',
        message='Домен rambler.ru запрещен',
        inverse_match=True)],
        unique=True
    )  # unique=True

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'age': self.age,
            'locations': [loc.name for loc in self.locations.all()]
        }
