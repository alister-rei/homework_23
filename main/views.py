import random

from django.core.cache import cache
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from blog.models import Post
from catalog.models import Product
from config import settings


class MainPage(TemplateView):
    template_name = 'main/main.html'
    extra_context = {
        'title': 'Skystore'
    }

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        if self.request.method == 'GET':
            if settings.CACHE_ENABLED:
                key = f'cached_statistics'
                cached_context = cache.get(key)
                if cached_context is None:
                    context = super().get_context_data(*args, **kwargs)
                    context['product_count'] = Product.objects.filter(is_published=True).count()
                    context['post_count'] = Post.objects.filter(is_published=True).count()

                    all_products = list(Product.objects.filter(is_published=True))
                    random.shuffle(all_products)
                    context['three_random_product'] = all_products[:3]

                    all_blog_posts = list(Post.objects.filter(is_published=True))
                    random.shuffle(all_blog_posts)
                    context['three_random_posts'] = all_blog_posts[:3]

                    main_page_context = {
                        'product_count': context['product_count'],
                        'post_count': context['post_count'],
                        'three_random_product': context['three_random_product'],
                        'three_random_posts': context['three_random_posts'],
                    }
                    cache.set(key, main_page_context)
                    return context
                else:
                    context = super().get_context_data(*args, **kwargs)
                    context['product_count'] = cached_context['product_count']
                    context['post_count'] = cached_context['post_count']
                    context['three_random_product'] = cached_context['three_random_product']
                    context['three_random_posts'] = cached_context['three_random_posts']
                    return context


class ContactsPageView(View):
    def get(self, request):
        context = {'title': 'Контакты'}
        return render(request, 'catalog/contacts.html', context)

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"name:{name}, phone:{phone}, message:{message}")
        context = {'title': 'Контакты'}
        return render(request, 'catalog/contacts.html', context)
