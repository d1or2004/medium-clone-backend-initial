from django.contrib.auth.models import AbstractUser
from django.db import models
from django_resized import ResizedImageField
import os
import uuid
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core import validators
from users.errors import BIRTH_YEAR_ERROR_MSG
from django.contrib.postgres.indexes import HashIndex


def file_upload(instance, filename):
    """ This function is used to upload the user's avatar. """
    ext = filename.split('.')[-1]
    filename = f'{instance.username}.{ext}'
    return os.path.join('users/avatars/', filename)


def thumbnail_file(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('users/thumbnails/', filename)


class CustomUser(AbstractUser):
    """  This model represents a custom user. """

    middle_name = models.CharField(max_length=30, blank=True, null=True)
    avatar = ResizedImageField(size=[300, 300], crop=['top', 'left'], upload_to=file_upload, blank=True)
    birth_year = models.IntegerField(
        validators=[  # tug'ilgan yil oralig'ini tekshirish uchun birinchi variant
            validators.MinValueValidator(settings.BIRTH_YEAR_MIN),
            validators.MaxValueValidator(settings.BIRTH_YEAR_MAX)
        ],
        null=True,
        blank=True
    )

    def clean(self):  # tug'ilgan yil oralig'ini tekshirish uchun ikkinchi variant
        super().clean()
        if self.birth_year and not (settings.BIRTH_YEAR_MIN < self.birth_year < settings.BIRTH_YEAR_MAX):
            raise ValidationError(BIRTH_YEAR_ERROR_MSG)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]
        # Composite Index va Hash Index qo'shish
        indexes = [
            HashIndex(fields=['first_name'], name='%(class)s_first_name_hash_idx'),
            HashIndex(fields=['last_name'], name='%(class)s_last_name_hash_idx'),
            HashIndex(fields=['middle_name'], name='%(class)s_middle_name_hash_idx'),
            models.Index(fields=['username'], name='%(class)s_username_idx'),
        ]

        constraints = [
            models.CheckConstraint(  # tug'ilgan yil oralig'ini tekshirish uchun uchunchi variant
                check=models.Q(birth_year__gt=settings.BIRTH_YEAR_MIN) & models.Q(
                    birth_year__lt=settings.BIRTH_YEAR_MAX),
                name='check_birth_year_range'
            )
        ]

    def __str__(self):
        """ This method returns the full name of the user"""
        if self.full_name:
            return self.full_name
        else:
            return self.email or self.username

    @property
    def full_name(self):
        """ Returns the user's full name. """
        return f"{self.last_name} {self.first_name} {self.middle_name}"


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


class Clap(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name="claps", on_delete=models.CASCADE)
