from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetDoneView

from django.core.mail import send_mail
from django.http import Http404
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView, ListView
from django.urls import reverse_lazy, reverse

from config import settings
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User, Group
from django.shortcuts import redirect, render
from django.contrib.auth import login


def is_member(user):
    return user.groups.filter(name='manager').exists()


class RegisterView(CreateView):
    """ Регистрация нового пользователя и его валидация через письмо на email пользователя """
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()

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
        return redirect('users:email_confirmation_sent')


class UserConfirmationSentView(PasswordResetDoneView):
    """ Выводит информацию об отправке на почту подтверждения регистрации """
    template_name = "users/registration_sent_done.html"
    extra_context = {
        'title': 'На почту отправлена ссылка подтверждения регистрации'
    }


class UserConfirmEmailView(View):
    """ Подтверждение пользователем регистрации """

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')


class UserConfirmedView(TemplateView):
    """ Выводит информацию об успешной регистрации пользователя """
    template_name = 'users/registration_confirmed.html'


class UserConfirmationFailView(View):
    """ Выводит информацию о невозможности зарегистрировать пользователя """
    template_name = 'users/email_confirmation_failed.html'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """ Контроллер профиля пользователя """
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    extra_context = {
        'title': 'Users list'
    }

    def test_func(self):
        # Получаем текущий объект продукта
        queryset = super().get_queryset()

        # Проверка доступа: только is_stuff
        return self.request.user.is_staff

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:  # для суперпользователя
            queryset = super().get_queryset()
        elif user.is_staff:
            queryset = super().get_queryset().filter(is_staff=False)
        else:  # для остальных пользователей
            queryset = None
        return queryset


def toggle_active(request, pk):
    if request.user.is_staff:
        user = User.objects.get(pk=pk)
        user.is_active = not user.is_active
        user.save()
        return redirect('users:user_list')


@login_required
def generate_new_password(request):
    """ Генерирует новый пароль пользователя """
    new_password = get_random_string(length=9)

    send_mail(
        subject='Новый пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )

    request.user.set_password(new_password)
    request.user.save()

    return redirect(reverse('users:main'))


def regenerate_password(request):
    """ Генерирует новый пароль пользователя """
    if request.method == 'POST':
        email = request.POST.get('email')
        # Получаем пользователя по email
        user = User.objects.get(email=email)

        # Генерируем новый пароль
        new_password = get_random_string(length=9)

        # Изменяем пароль пользователя
        user.set_password(new_password)
        user.save()

        # Отправляем письмо с новым паролем
        send_mail(
            subject='Восстановление пароля',
            message=f'Ваш новый пароль: {new_password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

        return redirect(reverse('users:main'))
    return render(request, 'users/regenerate_password.html')


class ModeratorCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'create_moderator.html'
    success_url = reverse_lazy('users:user_list')

    def test_func(self):
        # Проверка доступа: только суперпользователь
        return self.request.user.is_superuser

    def form_valid(self, form):
        user = form.save()
        user.is_active = True
        user.is_staff = True
        user.save()
        moderator_group = Group.objects.get(name='manager')
        user.groups.add(moderator_group)
        self.object = form.save()
        return super().form_valid(form)
