# Generated by Django 4.1.3 on 2022-11-26 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_remove_book_author_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='published',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
