from django.contrib import admin
from .models import Profile, Post, Like, Comment, Story, StoryItem, Follow


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name')
    search_fields = ('user__username', 'display_name')
    readonly_fields = ('user',)
    
    fieldsets = (
        ('사용자', {
            'fields': ('user',)
        }),
        ('프로필 정보', {
            'fields': ('display_name', 'bio', 'avatar')
        }),
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_at', 'updated_at')
    list_filter = ('created_at', 'author')
    search_fields = ('author__username', 'content')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('게시물 정보', {
            'fields': ('author', 'content', 'image')
        }),
        ('시간정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'post__author__username')
    readonly_fields = ('created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'created_at', 'updated_at')
    list_filter = ('created_at', 'author', 'post')
    search_fields = ('author__username', 'content')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_at', 'expires_at', 'is_active')
    list_filter = ('created_at', 'author')
    search_fields = ('author__username',)
    readonly_fields = ('created_at', 'is_active')


@admin.register(StoryItem)
class StoryItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'story', 'order', 'created_at')
    list_filter = ('story', 'order')
    readonly_fields = ('created_at',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following', 'created_at')
    list_filter = ('created_at', 'follower', 'following')
    search_fields = ('follower__username', 'following__username')
    readonly_fields = ('created_at',)
