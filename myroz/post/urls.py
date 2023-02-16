from django.urls import path

from . views import *
app_name = 'post_app'

urlpatterns = [
    path('', index, name='home'),
    path('groups/', groups),
    # Профайл пользователя
    path('profile/<str:username>/', profile, name='profile'),
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path('group/<slug:slug>/', group_posts, name='post_group'),
    path('create/', post_create, name='post_create')
]
