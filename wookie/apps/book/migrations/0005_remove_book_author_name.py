# Generated by Django 4.1.3 on 2022-11-25 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_book_author_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author_name',
        ),
    ]
