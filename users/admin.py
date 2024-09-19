from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Topic, Article


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # fieldsets = UserAdmin.fieldsets + (
    #     (None, {'fields': ('middle_name',)}),
    # )
    fieldsets = UserAdmin.fieldsets + (
        ('Additional info', {
            'fields': ('middle_name', 'avatar',)
        }),
    )
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'middle_name')
    list_display_links = ('id', 'username', 'email')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'middle_name')
    list_filter = ('last_login', 'date_joined', 'is_staff', 'is_superuser', 'is_active')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    list_display_links = ('name', 'description')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')
    search_fields = ('title', 'content')
    list_display_links = ('title', 'content')
