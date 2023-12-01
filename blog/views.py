from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Post
from main.services import is_member


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Post
    login_url = 'users:login'
    fields = ('title', 'description', 'image', 'is_published')
    success_url = reverse_lazy('blog:blog')
    extra_context = {
        'title': 'Create Post'
    }

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save(update_fields=['owner'])
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ('title', 'description', 'image', 'is_published')
    extra_context = {
        'title': 'Update Post'
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser:
            if self.object.owner != user or is_member(user):
                raise Http404
        return self.object

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.object.pk])


class BlogListView(ListView):
    model = Post
    extra_context = {
        'title': 'Blog'
    }

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:  # для зарегистрированных пользователей
            if user.is_staff or user.is_superuser:  # для работников и суперпользователя
                queryset = super().get_queryset().order_by('pk')

            else:  # для остальных пользователей
                # Получаем queryset, результат фильтрации по условию owner=user
                queryset_1 = super().get_queryset().filter(owner=user).order_by('pk')
                # Получаем queryset, результат фильтрации по условию is_published=True
                queryset_2 = super().get_queryset().filter(is_published=True).order_by('pk')
                # Объединяем два queryset с использованием метода union()
                queryset = queryset_2.union(queryset_1)

        else:  # для незарегистрированных пользователей
            queryset = super().get_queryset().filter(
                is_published=True, is_active=True).order_by('-pk')
        return queryset


class BlogDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        post.views_count += 1
        post.save(update_fields=['views_count'])
        context['title'] = post.title
        return context


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:blog')
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
