from django.shortcuts import render, get_object_or_404


from blog.models import Post


def post_list(request):
    posts = Post.published.all()
    context = {
        "posts": posts
    }
    return render(request=request,
                  template_name="blog/post/list.html",
                  context=context)


def post_detail(request, slug):
    post = get_object_or_404(Post,
                             slug=slug,
                             status=Post.Status.PUBLISHED)
    context = {
        "post": post
    }
    return render(request=request,
                  template_name="blog/post/detail.html",
                  context=context)


