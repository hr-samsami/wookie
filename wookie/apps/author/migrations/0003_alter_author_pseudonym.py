# Generated by Django 4.1.3 on 2022-11-25 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0002_alter_author_pseudonym'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='pseudonym',
            field=models.CharField(default='h.samsami', max_length=255),
            preserve_default=False,
        ),
    ]
