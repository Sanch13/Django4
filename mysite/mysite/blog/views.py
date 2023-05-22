from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    posts = Post.published.all()  # извлек. все посты со статусом PUBLISHED, исп. менеджер published
    return render(request=request,
                  template_name="blog/post/list.html",
                  context={"posts": posts})


def post_detail(request, id):
    # try:
    #     post = Post.objects.get(pk=id)  # извлек. объект Post с заданным id
    # except Post.DoesNotExist:
    #     raise Http404("No Post found")
    post = get_object_or_404(Post,
                             pk=id,
                             status=Post.Status.PUBLISHED)
    #  get_object_or_404 - функцию сокращенного доступа для вызова метода
    # get() в заданном модельном менеджере и вызова исключения Http404
    return render(request=request,
                  template_name="blog/post/detail.html",
                  context={"post": post})
