# Generated by Django 4.2.7 on 2023-11-28 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_published',
            field=models.BooleanField(choices=[(True, 'Опубликовано'), (False, 'На модерации')], default=True, verbose_name='Опубликовано'),
        ),
    ]