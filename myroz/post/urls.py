from django.urls import path

from .views import *
app_name = 'post_app'

urlpatterns = [
    path('', index, name='home'),
    path('groups/', groups),
    path('group/<slug:slug>/', group_posts, name='post_group')
]
