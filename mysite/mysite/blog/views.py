from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .froms import EmailPostForm
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# def post_list(request):
#     post_list = Post.published.all()  # извлек. все посты со статусом PUBLISHED, исп. менеджер
#     # published
#     # # Постраничная разбивка с 3 постами на страницу
#     paginator = Paginator(post_list, 3)  # paginator - экземпляр класса Paginator с числом объектов,
#     # возвращаемых в расчете на страницу
#     page_number = request.GET.get("page", 1)  # извлекаем HTTP GET-параметр page и сохраняем его в
#     # переменной page_number. Если параметра page нет в GET-параметрах запроса, используем
#     # стандартное значение 1, чтобы загрузить первую страницу результатов.
#     try:
#         posts = paginator.page(page_number)  # получ. объекты для желаем. стр., вызывая метод page()
#     except PageNotAnInteger:  # Если page_number не целое число, то выдать первую страницу
#         posts = paginator.page(1)
#     except EmptyPage:  # Если page_number находится вне диапазона, то выдать последнюю страницу
#         posts = paginator.page(paginator.num_pages)  # paginator.num_pages - общее число страниц
#     return render(request=request,
#                   template_name="blog/post/list.html",
#                   context={"posts": posts})

class PostListView(ListView):  # ListView позволяет перечислять объекты любого типа
    """    Альтернативное представление списка постов    """
    queryset = Post.published.all()  # атрибут queryset, нужен для того, чтобы иметь
    # конкретно-прикладной набор запросов QuerySet, не извлекая все объекты базы данных
    context_object_name = "posts"  # контекстная переменная posts исп. для результатов запроса
    # queryset. Если не указ. имя контекстного объекта то по умолчанию исп. переменная object_list
    paginate_by = 3  # задается постраничная разбивка результатов с возвратом 3 объектов на страницу
    template_name = "blog/post/list.html"  # путь + шаблон котор. исп. для прорисовки страницы


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
    return render(request=request,
                  template_name="blog/post/detail.html",
                  context={"post": post})


def post_share(request, post_id):
    """Извлечь пост по идентификатору post_id и PUBLISHED"""
    post = get_object_or_404(Post,  # Извлечь пост по идентификатору post_id и PUBLISHED
                             pk=post_id,
                             status=Post.Status.PUBLISHED)
    if request.method == "POST":  # Форма была передана на обработку
        form = EmailPostForm(data=request.POST)  # забираем данные из полей формы
        if form.is_valid():  # проверка корректно введены ли данные
            data = form.cleaned_data  # Сохраняем очищенные данные в data
            print(data)
            # Отправить пост на почту
    else:
        form = EmailPostForm()  # просто создаем форму ввода для данных и передаем на фронт
    return render(request=request,
                  template_name="blog/post/share.html",
                  context={"post": post, "form": form})
