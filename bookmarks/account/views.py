from django.shortcuts import render
from .forms import LoginForm, UserRegistrationForm
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


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(data=request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            print(new_user.__dict__)
            # Метод save() создает экземпляр модели, к которой форма привязана, и сохраняет его
            # в базе данных. Если вызывать его, используя commit=False, то экземпляр модели
            # создается, но не сохраняется в базе данных. Такой подход позволяет видоизменять
            # объект перед его окончательным сохранением.
            new_user.set_password(user_form.cleaned_data["password"])
            # Установить выбранный пароль
            new_user.save()
            print(new_user.__dict__)
            return render(request=request,
                          template_name="account/register_done.html",
                          context={"user_form": user_form})
    else:
        user_form = UserRegistrationForm()
    return render(request=request,
                  template_name="account/register.html",
                  context={"user_form": user_form})
