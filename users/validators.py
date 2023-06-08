import datetime

from rest_framework.exceptions import ValidationError


def check_age(value):
    today = datetime.date.today()
    age = (today.year - value.year - 1) + ((today.month, today.day) >= (value.month, value.day))
    if age < 9:
        raise ValidationError(f'Возраст не может быть менее 9 лет. Ваш возраст: {age}')
