from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from .forms import LoginForm


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
