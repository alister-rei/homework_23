# Generated by Django 4.2.7 on 2023-11-28 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('slug', models.CharField(blank=True, max_length=100, null=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Содержимое')),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog/', verbose_name='Изображение(превью)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('is_published', models.BooleanField(choices=[(True, 'Активна'), (False, 'На модерации')], default=True, verbose_name='Опубликовано')),
                ('views_count', models.IntegerField(default=0, verbose_name='просмотров')),
                ('is_active', models.BooleanField(choices=[(True, 'Активна'), (False, 'На модерации')], default=True, verbose_name='Активна')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Пост',
            },
        ),
    ]
