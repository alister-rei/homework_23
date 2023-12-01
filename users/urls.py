from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView

from users.apps import UsersConfig
from users.views import RegisterView, UserUpdateView, generate_new_password, UserConfirmEmailView, \
    UserConfirmationSentView, UserConfirmedView, UserConfirmationFailView, regenerate_password, UserListView, \
    toggle_active, ModeratorCreateView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('toggle-active/<int:pk>/', toggle_active, name='toggle_active'),
    path('create_moderator/', ModeratorCreateView.as_view(), name='create_moderator'),

    path('profile/genpassword/', generate_new_password, name='generate_new_password'),
    path('regenerations/', regenerate_password, name='regenerate_password'),
    path('email_confirmation_sent/', UserConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm_email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email_confirmed/', UserConfirmedView.as_view(), name='email_confirmed'),
    path('email_confirmation_failed/', UserConfirmationFailView.as_view(), name='email_confirmation_failed'),
]
