from rest_framework.exceptions import ValidationError


def check_not_published(value: bool) -> None:
    if value:
        raise ValidationError(f"Поле is_published не может быть {value}")
