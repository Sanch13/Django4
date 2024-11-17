import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from blog.managers.managers import PublishedManager


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    slug = models.SlugField(max_length=250, default=uuid.uuid4, unique=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return f"{self.title} {self.id}"

    def get_absolute_url(self):
        return reverse(viewname="blog:post_detail", args=[self.slug])
