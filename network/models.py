from django.contrib.auth.models import AbstractUser
from django.db import models

# importing datetime module 
import datetime 

class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=144)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content}"