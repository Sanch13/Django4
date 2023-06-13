from django.shortcuts import render,  redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForms


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
