from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.views import generic
from django.conf import settings
from django.views.decorators.http import require_POST

from blog.forms import EmailPostForm, CommentForm
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
    comments = post.comments.filter(active=True)
    print(comments)
    form = CommentForm()
    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }
    return render(request=request,
                  template_name="blog/post/detail.html",
                  context=context)


def post_share(request, slug):
    post = get_object_or_404(Post,
                             slug=slug,
                             status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        form_email = EmailPostForm(request.POST)
        if form_email.is_valid():
            cd = form_email.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'"{cd["name"]} recommends you read {post.title}"'
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject=subject,
                      message=message,
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[cd["to"]])
            sent = True
    else:
        form_email = EmailPostForm()

    return render(request=request,
                  template_name="blog/post/share.html",
                  context={"post": post, "form": form_email, "sent": sent}, )


@require_POST
def post_comment(request, slug):
    post = get_object_or_404(Post,
                             slug=slug,
                             status=Post.Status.PUBLISHED)

    comment = None
    form_comment = CommentForm(request.POST)
    if form_comment.is_valid():
        comment = form_comment.save(commit=False)
        comment.post = post
        comment.save()

    return render(request=request,
                  template_name="blog/post/comment.html",
                  context={'post': post,
                           'form': form_comment,
                           'comment': comment})


class PostListView(generic.ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    template_name = "blog/post/list.html"


class PostDetailView(generic.DetailView):
    queryset = Post.published.all()
    template_name = "blog/post/detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"  # Указываем, какой параметр из URL использовать

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Получаем стандартный контекст
        post = self.get_object()  # метод, который возвращает текущий объект
        comments = post.comments.filter(active=True)
        form = CommentForm()

        context['comments'] = comments
        context['form'] = form
        return context
