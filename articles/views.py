from rest_framework.viewsets import ModelViewSet
from .serializers import Article, ArticleCreateSerializer, ArticleDetailSerializer
from .models import Article
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class ArticlesView(ModelViewSet):
    """Maqolalarni yaratish va olish uchun API."""
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArticleDetailSerializer
        return ArticleCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_public and not request.user.is_staff:
            return Response({"detail": "Maqola hali ommaga ko'rsatilmaydi."}, status=403)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
