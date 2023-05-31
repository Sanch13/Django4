from django.shortcuts import render
from .forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.method == "POST":  # if method post?
        form = LoginForm(data=request.POST)  # get data from request
        if form.is_valid():  # check data from form
            username = form.cleaned_data["username"]  # get username from dict
            password = form.cleaned_data["password"]  # get password from dict
            user = authenticate(request, username=username, password=password)
            # check user into databases
            # authenticate возвращает объект User, если пользователь был успешно аутентифицирован,
            # либо None в противном случае.
            if user is not None:
                if user.is_active:
                    login(request=request, user=user)
                    return HttpResponse("Authenticated successfully")
                else:
                    return HttpResponse("Disable account")
            return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request=request,
                  template_name="account/login.html",
                  context={"form": form})


@login_required
def dashboard(request):
    return render(request=request,
                  template_name="account/dashboard.html",
                  context={"section": dashboard})
