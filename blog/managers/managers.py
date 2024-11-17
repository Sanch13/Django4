from django.db import models


class PublishedManager(models.Manager):
    """
    Class Manager provides public posts
    """
    def get_queryset(self):
        from blog.models import Post
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
