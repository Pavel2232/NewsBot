from django.contrib import admin
from .models import TgUser, News, Like, Comment


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'username', 'is_admin', 'created_at', 'updated_at')
    list_filter = ('is_admin', 'created_at', 'updated_at')
    search_fields = ('telegram_id', 'username')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('slug', 'owner', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('slug', 'owner__telegram_id')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('owner', 'news', 'like', 'created_at', 'updated_at')
    list_filter = ('like', 'created_at', 'updated_at')
    search_fields = ('owner__telegram_id', 'news__slug')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('owner', 'news', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('owner__telegram_id', 'news__slug')
