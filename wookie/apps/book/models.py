from django.contrib.auth import get_user_model
from django.core.validators import validate_image_file_extension
from django.db import models

USER_MODEL = get_user_model()


class Book(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=False, null=False)
    cover_image = models.ImageField(upload_to='books/covers', verbose_name='cover image', max_length=500,
                                    validators=[validate_image_file_extension],
                                    error_messages={'invalid_extension': '%(value)s'})
    author = models.OneToOneField(USER_MODEL, on_delete=models.CASCADE)
