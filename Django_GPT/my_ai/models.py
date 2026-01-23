from django.db import models
from django.conf import settings


class Conversation(models.Model):
    MODEL_CHOICES = (
        ("translate", "Translation"),
        ("sentiment", "Sentiment"),
        ("generate", "Text Generation"),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    model_type = models.CharField(max_length=20, choices=MODEL_CHOICES)
    
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    ROLE_CHOICES = (
        ("user", "user"),
        ("assistant", "assistant"),
    )

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
