from .models import Profile, Contact
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def index(request):
    return render(request=request, template_name="base.html")


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
            # Метод save() создает экземпляр модели, к которой форма привязана, и сохраняет его
            # в базе данных. Если вызывать его, используя commit=False, то экземпляр модели
            # создается, но не сохраняется в базе данных. Такой подход позволяет видоизменять
            # объект перед его окончательным сохранением.
            new_user.set_password(user_form.cleaned_data["password"])
            # Установить выбранный пароль
            new_user.save()
            Profile.objects.create(user=new_user)
            # При регистрации пользователей в системе будет создаваться объект Profile,
            # который будет ассоциирован с созданным объектом User.
            return render(request=request,
                          template_name="account/register_done.html",
                          context={"user_form": user_form})
    else:
        user_form = UserRegistrationForm()
    return render(request=request,
                  template_name="account/register.html",
                  context={"user_form": user_form})


@login_required  # только аутентифицированные пользователи могут редактировать свои профили
def edit(request):
    """чтобы пользователи могли редактировать свою личную информацию."""
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request=request,
                             message="Profile updated successfully")
        else:
            messages.error(request=request,
                           message="Error updated your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request=request,
                  template_name="account/edit.html",
                  context={"profile_form": profile_form,
                           "user_form": user_form})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request=request,
                  template_name="account/user/list.html",
                  context={"section": "people",
                           "users": users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request=request,
                  template_name="account/user/detail.html",
                  context={"section": "people",
                           "user": user})


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user)
                # create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})
