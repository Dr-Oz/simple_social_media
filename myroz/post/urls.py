from django.urls import path

from . views import *
app_name = 'post_app'

urlpatterns = [
    path('', index, name='home'),
    # Профайл пользователя
    path('profile/<str:username>/', profile, name='profile'),
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path('group/<slug:slug>/', group_posts, name='post_group'),
    path('create/', post_create, name='post_create'),
    path('posts/<int:post_id>/edit/', post_edit, name='post_edit'),
    path('posts/<int:post_id>/comment', add_comment, name='add_comment'),
]

handler404 = 'core.views.page_not_found'


