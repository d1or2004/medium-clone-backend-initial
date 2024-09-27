from .views import ArticlesView
from django.urls import path

urlpatterns = [
    path('articles/', ArticlesView.as_view({'get': 'list', 'post': 'create'}), name='articles-list-create'),
    path('articles/<int:pk>/', ArticlesView.as_view({'get': 'retrieve'}), name='article-detail'),
]
