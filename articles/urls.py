from .views import ArticlesView
from django.urls import path

urlpatterns = [
    path('articles/', ArticlesView.as_view({'get': 'list', 'post': 'create'}), name='articles-list-create'),
    # Maqolalarni ko'rish va yaratish
]
