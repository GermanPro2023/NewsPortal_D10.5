from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Author, User, SubscribersCategory
from datetime import datetime
from .filters import PostFilter, PostCategoryFilter
from django.views.generic.edit import CreateView
from .forms import PostForm, SubscribeForm
from django.urls import reverse_lazy
from django.shortcuts import render, reverse, redirect
from django.core.mail import send_mail
# from django.http import HttpResponse
# from .tasks import hello

class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    ordering = '-datetime_post' # Поле, которое будет использоваться для сортировки объектов
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


    # вот так мы можем указать количество записей на странице

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()

        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['filterset'] = self.filterset
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        return context

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — post.html
    ordering = '-datetime_post'
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'

class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'create.html'
    permission_required = 'news.add_post' #добавление права создание объекта

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/create/':
            post.types_post = 'NE'
        if self.request.path == '/article/create/':
            post.types_post = 'AR'
        return super().form_valid(form)

class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = 'news.change_post' #добавление права изменение содержание объекта


# Представление удаляющее товар.
class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class PostSearch(ListView):
    model = Post
    form = PostFilter
    template_name = 'search.html'
    context_object_name = 'search'

    def get_queryset(self):
        queryset = super(PostSearch, self).get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.queryset

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class SubscriberView(CreateView):
    model = SubscribersCategory
    form_class = SubscribeForm
    template_name = 'subscribe.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        subscribe = form.save(commit=False)
        subscribe.subscriber = User.objects.get(pk=self.request.user.id)
        return super(SubscriberView, self).form_valid(form)


# class IndexView(View):
#     def get(self, request):
#         printer.delay(10)
#         hello.delay()
#         return HttpResponse('Hello!')
