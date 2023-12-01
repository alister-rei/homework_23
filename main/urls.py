from django.urls import path
from main.apps import MainConfig
from main.views import MainPage, ContactsPageView

app_name = MainConfig.name

urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),
]
