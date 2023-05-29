from django import template
from django.db.models import Count
import markdown
from django.utils.safestring import mark_safe

from ..models import Post

register = template.Library()


# переменная register является экземпляром класса template.Library, и она
# используется для регистрации шаблонных тегов и фильтров приложения.


"""Django будет использовать имя функции в качестве имени тега."""


@register.simple_tag  # регистр. простой тег total_posts с помощью декоратора
def total_posts() -> int:
    """Возвращает кол-во постов"""
    return Post.published.count()


@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count: int = 5) -> dict:
    """Возвращает список последних постов"""
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}


@register.simple_tag
def get_most_commented_posts(count: int = 5) -> list:
    """Возвращает список (count) постов содерж. наибольшее кол-во коментариев к ним"""
    return Post.published.annotate(
        total_comments=Count("comments")).order_by("-total_comments")[:count]
    # Функция агрегирования Count используется для сохранения количества комментариев в вычисляемом
    # поле total_comments по каждому объекту Post


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
