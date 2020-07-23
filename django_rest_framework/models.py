from django.db import models


class Posts(models.Model):
    post_title = models.CharField(max_length=50)
    post_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


