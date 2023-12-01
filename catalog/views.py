from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import formset_factory, inlineformset_factory
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from catalog.forms import ProductForm, VersionForm, ManagerProductForm
from catalog.models import Product, Version
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from main.services import is_member


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    login_url = 'users:login'
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list')
    extra_context = {
        'title': 'Create Product'
    }

    def form_valid(self, form):
        new_mat = form.save()
        new_mat.slug = slugify(new_mat.name)
        new_mat.save(update_fields=['slug'])
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save(update_fields=['owner'])
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    extra_context = {
        'title': 'Update Product'
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser:
            if self.object.owner != user or is_member(user):
                raise Http404
        return self.object

    def get_form_class(self):
        return super().get_form_class()

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)

        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object, )
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        new_mat = form.save()
        new_mat.slug = slugify(new_mat.name)
        new_mat.save()
        self.object.save()
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:view', args=[self.object.pk])


class ManagerProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ManagerProductForm
    template_name = 'catalog/manager_update_product.html'
    permission_required = ['catalog.set_is_published', 'catalog.set_description', 'catalog.set_category']
    extra_context = {
        'title': 'Manager Update Product'
    }

    def form_valid(self, form):
        new_mat = form.save()
        new_mat.slug = slugify(new_mat.name)
        new_mat.save()
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:view', args=[self.object.pk])


class ProductListView(ListView):
    model = Product
    extra_context = {
        'title': 'Skystore'
    }

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:  # для зарегистрированных пользователей
            if user.is_staff or user.is_superuser:  # для работников и суперпользователя
                queryset = super().get_queryset().order_by('pk')

            else:  # для остальных пользователей
                # Получаем queryset, результат фильтрации по условию owner=user
                queryset_1 = super().get_queryset().filter(owner=user)
                # Получаем queryset, результат фильтрации по условию is_published=True
                queryset_2 = super().get_queryset().filter(is_published=True)
                # Объединяем два queryset с использованием метода union()
                queryset = queryset_2.union(queryset_1)
                # queryset = super().get_queryset().filter(owner=user).order_by('pk')

        else:  # для незарегистрированных пользователей
            queryset = super().get_queryset().filter(
                is_published=True).order_by('-pk')
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        for product in context['object_list']:
            active_version = product.version_set.filter(is_current=True).first()
            if active_version:
                product.active_version_number = active_version.version_number
                product.active_version_name = active_version.version_name
            else:
                product.active_version_number = None
                product.active_version_name = None
        return context


class MyProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'catalog/list.html'
    extra_context = {
        'title': 'My Product'
    }

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().filter(owner=user).order_by('pk')
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        for product in context['object_list']:
            active_version = product.version_set.filter(is_current=True).first()
            if active_version:
                product.active_version_number = active_version.version_number
                product.active_version_name = active_version.version_name
            else:
                product.active_version_number = None
                product.active_version_name = None
        return context


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['title'] = product.name
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:list')
    extra_context = {
        'title': 'Delete Post'
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser:
            if self.object.owner != user or is_member(user):
                raise Http404
        return self.object


def toggle_active(request, pk):
    if request.user.is_staff:
        product = Product.objects.get(pk=pk)
        product.is_published = not product.is_published
        product.save(update_fields=['is_published'])
        return redirect('catalog:list')
