from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import Group, Permission
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from config import settings


def is_member(user):
    return user.groups.filter(name='manager').exists()


def send_verify_code(user):
    # формируем токен и ссылку для подтверждения регистрации
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_url = reverse_lazy('users:confirm_email', kwargs={'uidb64': uid, 'token': token})

    current_site = '127.0.0.1:8000'

    send_mail(
        subject='Регистрация на платформе',
        message=f"Завершите регистрацию, перейдя по ссылке: http://{current_site}{activation_url}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email]
    )


def mail_sender(subject, message, email):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )


def create_manager():
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

