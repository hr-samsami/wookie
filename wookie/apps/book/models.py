from django.contrib.auth import get_user_model
from django.core.validators import validate_image_file_extension, MinLengthValidator
from django.db import models

USER_MODEL = get_user_model()


class Book(models.Model):
    author = models.ForeignKey(USER_MODEL, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255, db_index=True, validators=[MinLengthValidator(3)])
    description = models.TextField(validators=[MinLengthValidator(3)])
    cover_image = models.ImageField(upload_to='images/book-covers', verbose_name='cover image', max_length=500,
                                    validators=[validate_image_file_extension],
                                    error_messages={'invalid_extension': '%(value)s'}, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    published = models.BooleanField(blank=True, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published']

    @property
    def author_pseudonym(self):
        return self.author.pseudonym

    def __str__(self):
        return self.title
