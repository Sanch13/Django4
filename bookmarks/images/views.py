from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForms
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from actions.utils import create_action
import redis
from django.conf import settings

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


@login_required
def image_create(request):
    if request.method == "POST":
        form = ImageCreateForms(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)  # create new instance without saving to DB
            new_image.user = request.user  # current user from request
            new_image.save()  # save instance to DB
            create_action(user=request.user,
                          verb="bookmarked_image",
                          target=new_image)
            messages.success(request=request, message="Image added successfully")
            return redirect(to=new_image.get_absolute_url())
    else:
        form = ImageCreateForms(data=request.GET)
    return render(request=request,
                  template_name="images/image/create.html",
                  context={"section": "images",
                           "form": form})


def image_detail(request, id, slug):
    """Display one image"""
    image = get_object_or_404(Image, id=id, slug=slug)
    total_views = r.incr(f"image:{image.id}:views")
    # команда incr, которая увеличивает значение данного ключа на 1. Если ключ не существует, то
    # команда incr его создает. incr() возвращает окончат. знач. ключа после выполнения операции.
    r.zincrby("image_ranking", 1, image.id)
    # Команда zincrby() используется для сохранения просмотров изображений в сортированном
    # множестве с ключом image:ranking. В нем будут храниться id изображения и соответствующий
    # балл, равный 1, который будет добавлен к общему баллу этого элемента сортированного множества.
    return render(request=request,
                  template_name="images/image/detail.html",
                  context={"section": "images",
                           "image": image,
                           "total_views": total_views})


@login_required
def image_ranking(request):
    # zrange() вернет все элементы сортированного множества
    image_ranking = r.zrange("image_ranking", 0, -1, desc=True)[:10]
    # получаем список id
    image_ranking_ids = [int(id) for id in image_ranking]
    print(image_ranking_ids)
    # извлекаем список объектов из БД
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    # сортировка объектов Image по индексу их появления в рейтинге изображений.
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    print(most_viewed)
    return render(request=request,
                  template_name="images/image/ranking.html",
                  context={'section': 'images',
                           'most_viewed': most_viewed})


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == "like":
                image.users_like.add(request.user)
                create_action(user=request.user,
                              verb="likes",
                              target=image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse(data={"status": "Ok"})
        except Image.DoesNotExist:
            pass
        return JsonResponse(data={"status": "error"})
