from django.contrib.auth.models import User
from django.db import models


class Posts(models.Model):
    post_title = models.CharField(max_length=50)
    post_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class BlackListedToken(models.Model):
    token = models.CharField(max_length=500)
    user_id = models.TextField(default=1)
    timestamp = models.DateTimeField(auto_now=True)

