# Generated by Django 4.2.1 on 2023-06-06 18:59

import django.core.validators
from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_birth_date_alter_user_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="birth_date",
            field=models.DateField(
                blank=True, null=True, validators=[users.validators.check_age]
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                max_length=254,
                validators=[
                    django.core.validators.RegexValidator(
                        inverse_match=True,
                        message="Домен rambler.ru запрещен",
                        regex="@rambler.ru",
                    )
                ],
            ),
        ),
    ]