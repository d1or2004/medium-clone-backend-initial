from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import os
import uuid
from users.models import CustomUser


def thumbnail_file(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('users/thumbnails/', filename)


class Topic(models.Model):
    """Maqola mavzularini saqlash uchun model."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"
        db_table = 'topic'


class Article(models.Model):

    """Maqolalarni saqlash uchun model."""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('published', 'Published'),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=255)
    summary = models.TextField()
    content = models.TextField()
    thumbnail = models.ImageField(upload_to=thumbnail_file, blank=True, null=True)
    topics = models.ManyToManyField(Topic, related_name='articles')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    is_public = models.BooleanField(default=False)  # Maqola tasdiqlanganligini ko'rsatadi
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Article"
        db_table = "article"


class Clap(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name="claps", on_delete=models.CASCADE)
