from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from .forms import ImageCreateForm
from .models import Image
from common.decorators import ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def image_create(request):
    if request.POST:
        # получает начальные данные и создает объект формы. Эти данные содер-
        # жат url и title картинки со стороннего сайта, они будут переданы в ка-
        # честве аргументов GET-запроса JavaScript-инструментом, который мы до-
        # бавим чуть позже. Пока подразумеваем, что данные будут
        form = ImageCreateForm(data=request.POST)
        # если форма отправлена POST-запросом, проверяет ее корректность. Если
        # данные валидны, создает новый объект Image, но пока не сохраняет его
        # в базу данных, передавая аргумент commit=False
        if form.is_valid():
            cd = form.cleaned_data

            new_item = form.save(commit=False)
            # Добавляем пользователя к созданному обьекту.
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image added successfully')
            # Перенаправляем пользователя на страницу сохранённого изобрадения
            return redirect(new_item.get_absolute_url())
    else:
        # Заполняем форму из GET-запроса.
        form = ImageCreateForm(data=request.GET)
    return render(request, 'images/image/create.html', {'section': 'images', 'form': form})

def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html', {'section': 'images', 'image': image})


@ajax_required
@login_required
@require_POST
# Декоратор login_required
# не даст неавторизованным пользователям доступ к этому обработчику. Деко-
# ратор require_POST возвращает ошибку HttpResponseNotAllowed (статус ответа 405),
# если запрос отправлен не методом POST. Таким образом, обработчик будет вы-
# полняться только при POST-запросах.
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    print('Функция сработала')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ok'})


# Функция проверки типа запроса
def is_ajax(request):
  return request.headers.get('x-requested-with') == 'XMLHttpRequest'

# В этом обработчике мы формируем QuerySet для получения всех изобра-
# жений, сохраненных в закладки. Затем создаем объект Paginator и получаем
# постраничный список картинок. Если желаемой страницы не существует, об-
# рабатываем исключение EmptyPage. В случае AJAX-запроса возвращаем пустое
# значение, чтобы остановить дальнейшую прокрутку списка картинок. Пере-
# даем контекст в два HTML-шаблона:
#  для AJAX-запросов используем list_ajax.html. Он содержит только HTML
# для показа картинок;
#  для стандартных запросов используем list.html. Этот шаблон наследует-
# ся от base.html и показывает полноценную страницу, на которую добав-
# лен список картинок из list_ajax.html.
# Добавьте URL-шаблон для этого обработчика
@login_required
def image_list(request):

    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # Если переданная страница не является числом, возвращаем первую.
        images = paginator.page(1)
    except EmptyPage:
        if is_ajax(request):
            # Если получили AJAX-запрос с номером страницы, большим, чем их количество, возвращаем пустую стоаницу.
            return HttpResponse('')
        # Если номер страницы больше, чем их количество, возвращаем последнюю.
        images = paginator.page(paginator.num_pages)
    if is_ajax(request):
        return render(request, 'images/image/list_ajax.html',
                      {'section': 'images', 'images': images})

    return render(request, 'images/image/list.html',
                  {'section': 'images', 'images': images})
