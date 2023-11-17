from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image


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
