from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.conf import settings
from django.views.decorators.http import require_POST
from .froms import EmailPostForm, CommentForm, SearchForm
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector


def index(request):
    return render(request=request, template_name="blog/base.html")


def post_list(request, tag_slug=None):
    post_list = Post.published.all()  # извлек. все посты со статусом PUBLISHED,
    # исп. менеджер published
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)  # извлекаем tag если он есть
        post_list = post_list.filter(tags__in=[tag])  # извлекаем все посты которые
        # содержат определенный tag . операция __in поиска по полю
    # Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(post_list, 3)  # paginator - экземпляр класса Paginator с числом объектов,
    # возвращаемых в расчете на страницу
    page_number = request.GET.get("page", 1)  # извлекаем HTTP GET-параметр page и сохраняем его в
    # переменной page_number. Если параметра page нет в GET-параметрах запроса, используем
    # стандартное значение 1, чтобы загрузить первую страницу результатов.
    try:
        posts = paginator.page(page_number)  # получ. объекты для желаем. стр., вызывая метод page()
    except PageNotAnInteger:  # Если page_number не целое число, то выдать первую страницу
        posts = paginator.page(1)
    except EmptyPage:  # Если page_number находится вне диапазона, то выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)  # paginator.num_pages - общее число страниц
    return render(request=request,
                  template_name="blog/post/list.html",
                  context={"posts": posts, "tag": tag})


# class PostListView(ListView):  # ListView позволяет перечислять объекты любого типа
#     """    Альтернативное представление списка постов    """
#     # def __init__(self, *args, **kwargs):
#     #     self.tag_slug = kwargs.pop("tag_slug", None)
#     #     super(PostListView, self).__init__(*args, **kwargs)
#     #
#     # if tag_slug:
#
#     queryset = Post.published.all()  # атрибут queryset, нужен для того, чтобы иметь
#     # конкретно-прикладной набор запросов QuerySet, не извлекая все объекты базы данных
#     context_object_name = "posts"  # контекстная переменная posts исп. для результатов запроса
#     # queryset. Если не указ. имя контекстного объекта то по умолчанию исп. переменная object_list
#     paginate_by = 3  # задается постраничная разбивка результатов с возвратом 3 объектов на страницу
#     template_name = "blog/post/list.html"  # путь + шаблон котор. исп. для прорисовки страницы


def post_detail(request, year, month, day, post):
    # try:
    #     post = Post.objects.get(pk=id)  # извлек. объект Post с заданным id
    # except Post.DoesNotExist:
    #     raise Http404("No Post found")
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=post)
    #  get_object_or_404 - функцию сокращенного доступа для вызова метода
    # get() в заданном модельном менеджере и вызова исключения Http404
    comments = post.comments.filter(active=True)
    # извлекаем все активные комментарии к посту. используем объект post, чтобы извлекать
    # связанные объекты Comment.используя атрибут related_name поля ForeignKey в модели Post
    form = CommentForm()

    post_tags_ids = post.tags.values_list("id", flat=True)
    # получаем список идентификаторов (id) тегов, связанных с определенным постом (post).
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(pk=post.id)
    # фильтруем все посты, которые имеют хотя бы один общий тег с исходным постом.
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by("-same_tags",
                                                                             "-publish")[:4]
    # выполняем annotate на результате фильтрации similar_posts.  Count("tags") подсчитывает
    # количество связанных тегов (tags) для каждого поста и сохр. кол-во в нов. пер same_tags
    # сортируем по кол-ву связ. тегов и публикации и нарезается чтобы получ. только 4 поста
    return render(request=request,
                  template_name="blog/post/detail.html",
                  context={"post": post, "form": form, "comments": comments,
                           "similar_posts": similar_posts})


def post_share(request, post_id):
    """Извлечь пост по идентификатору post_id и PUBLISHED"""
    post = get_object_or_404(Post,  # Извлечь пост по идентификатору post_id и PUBLISHED
                             pk=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False  # использ. sent в шаблоне для отображения сообщения об успехе или нет

    if request.method == "POST":  # Форма была передана на обработку
        form = EmailPostForm(data=request.POST)  # забираем данные из полей формы
        if form.is_valid():  # проверка корректно введены ли данные
            data = form.cleaned_data  # Сохраняем очищенные данные в data
            print(data)
            post_url = request.build_absolute_uri(post.get_absolute_url())
            # post_url - полный URL-адрес, включая HTTP-схему и хост-имя
            subject = f"{data['name']} recommends you read {post.title}"
            # заголовок письма
            message = f"Read {post.title} at {post_url} \n\n {data['name']}'s comments: " \
                      f"{data['comments']}"
            # текст сообщения электронного письма
            send_mail(subject=subject,
                      message=message,
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[data["to"]])
            sent = True  # письмо отправлено, меняем перемен. для вывода сообщения об успехе
            # Список ошибок валидации можно получить посредством form.errors.
    else:
        form = EmailPostForm()  # просто создаем форму ввода для данных и передаем на фронт
    return render(request=request,
                  template_name="blog/post/share.html",
                  context={"post": post, "form": form, "sent": sent}, )


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    comment = None  # перем. будет исп. для хранения комментарного объекта при его создании
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        # Метод save() создает экземпляр модели, к которой форма привязана, и сохраняет его в базе
        # данных. Если вызывать его, используя commit=False, то экземпляр модели создается, но не
        # сохраняется в базе данных. Такой подход позволяет видоизменять объект перед его
        # окончательным сохранением.
        comment.post = post
        comment.save()
    return render(request=request,
                  template_name="blog/post/comment.html",
                  context={"post": post, "form": form, "comment": comment})


def post_search(request):
    form = SearchForm()  # экземпляр формы SearchForm
    query = None  #
    results = []
    if "query" in request.GET:  # есть ли query в get запросе? Для проверки того, что форма была
        # передана на обработку, в словаре request.GET. если нет то форма рендериться пустая
        form = SearchForm(request.GET)  # создается ее экземпляр, используя переданные данные GET
        if form.is_valid():  # проверяется валидность данных формы
            query = form.cleaned_data["query"]  # забираем value из очищенного словаря
            results = Post.published.annotate(search=SearchVector("title", "body"), ).filter(
                search=query)  # выполняется поиск опубликованных постов в которых есть query
    return render(request=request,
                  template_name="blog/post/search.html",
                  context={"form": form,
                           "query": query,
                           "results": results})
