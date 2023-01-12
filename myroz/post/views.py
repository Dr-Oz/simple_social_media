

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse('Главня страница')

def groups(request):
    return HttpResponse('Список групп')

def group_posts(request, group_slug):
    return HttpResponse('Посты группы')

