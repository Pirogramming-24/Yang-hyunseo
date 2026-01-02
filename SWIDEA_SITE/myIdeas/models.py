from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class DevTool(models.Model):
    name = models.CharField(max_length=30, unique=True)
    type = models.CharField(max_length=30)
    explain = models.TextField()

    def __str__(self):
        return self.name

class Idea(models.Model):
    title = models.CharField(max_length=32)
    image = models.ImageField(
        upload_to='thumbNail_pics',
        default='default.jpg'
    )
    content = models.TextField()
    interest = models.IntegerField()
    devtool = models.ForeignKey(
        DevTool,
        on_delete=models.CASCADE
    )
    interestAmount = models.IntegerField()
    
    
class IdeaStar(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)


