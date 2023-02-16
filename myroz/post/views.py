import datetime

from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post, Group, User
from django.urls import reverse


# Create your views here.
def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    # Если порядок сортировки определен в классе Meta модели,
    # запрос будет выглядить так:
    # post_list = Post.objects.all()
    # Показывать по 10 записей на странице.
    paginator = Paginator(post_list, 3)

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    # Отдаем в словаре контекста
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'post/index.html', context)


def groups(request):
    template = 'post/group_list.html'
    text = 'Здесь будет информация о группах проекта Myroz'
    context = {
        'text': text
    }
    return render(request, template, context)


# View-функция для страницы сообщества:
def group_posts(request, slug):
    # Функция get_object_or_404 получает по заданным критериям объект
    # из базы данных или возвращает сообщение об ошибке, если объект не найден.
    # В нашем случае в переменную group будут переданы объекты модели Group,
    # поле slug у которых соответствует значению slug в запросе
    group = get_object_or_404(Group, slug=slug)

    # Метод .filter позволяет ограничить поиск по критериям.
    # Это аналог добавления
    # условия WHERE group_id = {group_id}
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'post/group_list.html', context)

def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    user = User.objects.get(username=username)
    post_user = Post.objects.filter(author=user).order_by('-pub_date')
    post_one = Post.objects.filter(author=user).order_by('-pub_date')[:1]
    paginator = Paginator(post_user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'username': username,
        'page_obj': page_obj,
        'post_user': post_user,
        'post_one': post_one,
    }
    return render(request, 'post/profile.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = post.author
    post_user = Post.objects.filter(author=user).order_by('-pub_date')
    context = {
        'post': post,
        'post_user': post_user
    }
    return render(request, 'post/post_detail.html', context)

def post_create(request):

    if request.method == 'POST':
        id = request.user.id
        author_id = User.objects.get(id=id)
        username = request.user.username
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = author_id
            post.save()
            return redirect('post_app:profile', username)

    form = PostForm()
    context = {
        "form": form,
    }
    return render(request, 'post/create_post.html', context)


