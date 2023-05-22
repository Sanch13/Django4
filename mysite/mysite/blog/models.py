from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    """новый конкретно-прикладной менеджер, чтобы извлекать все посты, имеющие статус PUBLISHED"""

    def get_queryset(self):  # переопределили этот метод
        """Метод get_queryset() менеджера PublishedManager возвращает набор запросов QuerySet,
        фильтрующий посты  только со статусом PUBLISHED"""
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        """перечисляемый класс Status путем подклассирования класса models.TextChoices."""
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="blog_posts")
    # related_name, чтобы указывать имя обратной связи, от User к Post. Такой подход позволит
    # легко обращаться к связанным объектам из объекта User, используя обозначение user.blog_posts
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    # status, является экземпляром типа CharField. Оно содержит параметр choices, чтобы
    # ограничивать значение поля вариантами из Status.choices.

    objects = models.Manager()  # менеджер, применяемый по умолчанию
    published = PublishedManager()  # конкретно-прикладной менеджер

    class Meta:  # Meta-класс определяет метаданные модели
        ordering = ["-publish"]  # порядок извлечении объектов из базы данных
        # от самых новых к самым старым постам
        indexes = [
            models.Index(fields=["-publish"])  # опция indexes позволяет определять в модели
            # индексы базы данных, которые могут содержать одно или несколько полей или
            # функциональные выражения и функции базы данных
        ]

    def __str__(self):
        return f"{self.title}"
