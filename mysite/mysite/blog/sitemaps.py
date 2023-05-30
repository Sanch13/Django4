from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq = "weekly"   # указывают частоту изменения страниц постов
    priority = 0.9  # релевантность на веб-сайте (максимальное значение равно 1)

    def items(self) -> list:
        """возвращает набор запросов QuerySet объектов, подлежащих включению в эту карту сайта"""
        return Post.published.all()

    def lastmod(self, obj):
        """возвращает время последнего изменения объекта"""
        return obj.updated
