from django.urls import path
from .views import PostListViews, PostDetailViews


urlpatterns = [
    path('', PostListViews.as_view(), name='blog_list'),
    path('<str:id>/<slug:slug>/', PostDetailViews.as_view(), name='blog_details'),
]
