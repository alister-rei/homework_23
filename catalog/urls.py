from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import ProductCreateView, ProductDetailView, ProductListView, ProductUpdateView, ProductDeleteView, \
    MyProductListView, toggle_active, ManagerProductUpdateView

app_name = CatalogConfig.name

urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='create'),
    path('', ProductListView.as_view(), name='list'),
    path('view/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='view'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
    path('my_product', MyProductListView.as_view(), name='my_product'),
    path('toggle-active/<int:pk>/', toggle_active, name='toggle_active'),
    path('moderating/<int:pk>/', ManagerProductUpdateView.as_view(), name='moderating'),
]
