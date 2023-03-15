from django.conf import settings
from django.conf.urls.static import static
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
    path("follow/", follow_index, name="follow_index"),
    path("<str:username>/follow/", profile_follow, name="profile_follow"),
    path("<str:username>/unfollow/", profile_unfollow, name="profile_unfollow"),
]

handler404 = 'core.views.page_not_found'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
