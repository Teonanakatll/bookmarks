from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from .forms import LoginForm, UserRegistrstionForm, UserEditForm, ProfileEditForm

from .models import Profile


def user_login(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # сверяем с данными в базе с помощью функции authenticate(). Она принимает аргументы request, username
            # и passwordи возвращает объект пользователя User, если он успешно аутентифицирован.В противном случае
            # вернется None. Если пользователь не был аутентифицирован, возвращаем объект HttpResponse с сообщением
            # о некорректном логине или пароле
            user = authenticate(request, username=cd['username'], password=cd['password'])
            # Если юзер существует
            if user is not None:
                # если пользователь был аутентифицирован, проверяем, активен ли он, через атрибут модели пользователя
                # Django, is_active (не заблокирован). Если пользователь неактивный, возвращаем HttpResponse
                # с соответствующим сообщением;
                if user.is_active:
                    # если пользователь активный, авторизуем его на сайте. Это происходит
                    # посредством вызова функции login(), которая запоминает пользователя
                    # в сессии. Затем возвращаем HttpResponse с сообщением об успешной авторизации.
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    # Наш обработчик обернут в декоратор login_required. Он проверяет, авторизован ли пользователь. Если пользователь
    # авторизован, Django выполняет обработку. В противном случае пользователь перенаправляется на страницу логина.
    # При этом в GET-параметре задается next -адрес запрашиваемой страницы. Таким образом, после успешного прохождения
    # авторизации пользователь будет перенаправлен на страницу, куда он пытался попасть.

    # Также мы добавили переменную контекста section, с помощью которой смо-
    # жем узнать, какой раздел сайта сейчас просматривает пользователь.
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.POST:
        user_form = UserRegistrstionForm(request.POST)
        if user_form.is_valid():
            # Создаём нового пользователя, но пока не сохраняем в базу данных.
            new_user = user_form.save(commit=False)
            # Задаём пользователю зашифрованный пароль.
            new_user.set_password(user_form.cleaned_data['password'])

            # Создание профиля пользователя.
            Profile.objects.create(user=new_user)

            # Сохраняем пользователя в базе данных.
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrstionForm()
    return render(request, 'account/register.html', {'user_form': user_form})

# Мы обернули функцию в декоратор login_required, потому что для измене-
# ния профиля пользователь должен быть авторизован.
@login_required
def edit(request):
    if request.POST:
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})
