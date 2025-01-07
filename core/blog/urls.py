from django.urls import path

from .views import PostDetailViews, PostListViews

urlpatterns = [
    path('<str:id>/<slug:slug>/', PostDetailViews.as_view(), name='blog_details'),
    path('', PostListViews.as_view(), name='blog_list'),
]
