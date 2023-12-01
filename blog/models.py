from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Post(models.Model):
    ACTIVE_CHOICES = ((True, 'Активна'), (False, 'На модерации'))

    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.CharField(max_length=100, **NULLABLE, verbose_name='Slug')
    description = models.TextField(**NULLABLE, verbose_name='Содержимое')
    image = models.ImageField(upload_to='blog/', **NULLABLE, verbose_name='Изображение(превью)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, choices=ACTIVE_CHOICES, verbose_name='Опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='просмотров')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.title}, {self.slug}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пост'
