import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post


class LatestPostsFeed(Feed):
    """подкласс класса Feed фреймворка синдицированных новостных лент"""
    title = "My Blog"
    link = reverse_lazy("blog:post_list")  # reverse_lazy() используется для того, чтобы
    # генерировать URL-адрес для атрибута link
    description = "New posts of my blog"

    def items(self) -> list:
        """извлекаем последние пять опубликованных постов"""
        return Post.published.all()[:5]

    # Методы item_title(), item_description() и item_pubdate() будут получать каждый
    # возвращаемый методом items() объект и возвращать заголовок, описание и
    # дату публикации по каждому элементу.

    def item_title(self, item):
        """возвращает заголовок из объекта item"""
        return item.title

    def item_description(self, item):
        """возвращает описание (30 символов) из объекта item"""
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item):
        """возвращает дату публикации из объекта item"""
        return item.publish
