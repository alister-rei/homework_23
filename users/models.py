from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group, Permission

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


# Создаем группу модераторов
moderator_group, created = Group.objects.get_or_create(name='manager')

# Определяем доступы
can_cancel_product = Permission.objects.get(codename='set_is_published')
can_change_product_description = Permission.objects.get(codename='set_description')
can_change_product_category = Permission.objects.get(codename='set_category')

# Добавляем доступы к группе модераторов
moderator_group.permissions.add(can_cancel_product)
moderator_group.permissions.add(can_change_product_description)
moderator_group.permissions.add(can_change_product_category)
