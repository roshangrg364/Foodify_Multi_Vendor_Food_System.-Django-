from django.core.exceptions import ValidationError
import os


def validate_images(value):
    extension = os.path.splitext(value.name)[1]
    valid_extensions = ["jpg", "png", ".jpeg"]
    if not extension.lower() in valid_extensions:
        raise ValidationError(
            "Unsupported Image Extension. Allowed Extensions:" + str(valid_extensions)
        )
