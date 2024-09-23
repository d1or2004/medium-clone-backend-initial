from .models import Article, Topic, Clap
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    """Author uchun serializer."""

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'middle_name', 'email', 'avatar']


class TopicSerializer(serializers.ModelSerializer):
    """Topic uchun serializer."""

    class Meta:
        model = Topic
        fields = ['id', 'name', 'description', 'is_active']


class ArticleCreateSerializer(serializers.ModelSerializer):
    """Maqolani yaratish uchun serializer."""
    author = AuthorSerializer(read_only=True)
    topics = TopicSerializer(many=True, read_only=True)
    topic_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Topic.objects.all(), write_only=True, source='topics'
    )

    class Meta:
        model = Article
        fields = ['id', 'author', 'title', 'summary', 'content', 'thumbnail', 'topics', 'topic_ids', 'status',
                  'created_at', 'updated_at']

    def create(self, validated_data):
        topic_ids = validated_data.pop('topics')
        article = Article.objects.create(**validated_data)
        article.topics.set(topic_ids)
        return article


# Clap modeli uchun serializer
class ClapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clap
        fields = ['id', 'user', 'article']


# Maqola detallari uchun serializer
class ArticleDetailSerializer(serializers.ModelSerializer):
    topic = TopicSerializer()  # Alohida serialayzer ishlatish
    claps = ClapSerializer(many=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'topic', 'claps', 'created_at', 'is_public']
