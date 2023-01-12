from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('groups/', groups),
    path('groups/<slug:group_slug>/', group_posts)
]
