
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Conversation, Message



@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "model_type", "created_at")
    list_filter = ("model_type",)
    search_fields = ("user__username",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "role", "short_content")
    list_filter = ("role",)
    search_fields = ("content",)

    def short_content(self, obj):
        return obj.content[:30]
    short_content.short_description = "Content"
