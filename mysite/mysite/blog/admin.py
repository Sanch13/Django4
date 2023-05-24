from django.contrib import admin
from .models import Post, Comment


# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "publish", "status"]  # позволяет задавать поля
    # модели, которые вы хотите показывать на странице django admin
    list_filter = ["status", "created", "publish", "author"]  # позволяет фильтровать результаты
    # по полям
    search_fields = ["title", "body"]  # поиск по полям
    prepopulated_fields = {"slug": ("title",)}  # автомат. заполнять поле slug данными поле title
    raw_id_fields = ["author"]  # поле author отображается поисковым виджетом
    date_hierarchy = "publish"  # для навигации по иерархии дат
    ordering = ["status", "publish"]  # критерии сортировки по умолчанию


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
