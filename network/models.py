from django.contrib.auth.models import AbstractUser
from django.db import models

# importing datetime module 
import datetime 

class User(AbstractUser):
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)

class Post(models.Model):
    content = models.CharField(max_length=144)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content}"

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="follower")
    profile = models.ForeignKey(User, on_delete=models.PROTECT, related_name="followed")

    class Meta:
        unique_together = ('user', 'profile')