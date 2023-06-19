from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForms
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST


@login_required
def image_create(request):
    if request.method == "POST":
        form = ImageCreateForms(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)  # create new instance without saving to DB
            new_image.user = request.user  # current user from request
            new_image.save()  # save instance to DB
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
    return render(request=request,
                  template_name="images/image/detail.html",
                  context={"section": "images",
                           "image": image})


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    # print("1", type(action), action, action.__dict__)
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == "like":
                image.users_like.add(request.user)
                # print("2", type(image), image, image.__dict__)
            else:
                image.users_like.remove(request.user)
            return JsonResponse(data={"status": "Ok"})
        except Image.DoesNotExist:
            pass
        return JsonResponse(data={"status": "error"})
