from django import forms
from .models import Image

from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    """Мы переопределили метод save(), оставив параметры оригинального метода класса ModelForm."""
    # В дополнение к валидации URL необходимо загрузить файл и сохранить
    # его. Для этого, например, мы могли бы реализовать обработчик, который
    # будет заполнять форму и скачивать изображение. Но мы пойдем по более
    # известному пути и переопределим метод save() модельной формы, чтобы
    # выполнять это действие при любом сохранении формы, а не только в кон-
    # кретном обработчике.
    def save(self, force_insert=False, force_update=False, commit=True):
        # создает объект image, вызвав метод save() с аргументом commit=False;
        # Если commit равен False, метод вернет объект модели, но не сохранит его.
        image = super(ImageCreateForm, self).save(commit=False)
        # получает URL из атрибута cleaned_data формы;
        image_url = self.cleaned_data['url']
        # генерирует название изображения, совмещая слаг и расширение картинки
        image_name = f"{slugify(image.title)}.{image_url.rsplit('.', 1)[1].lower()}"

        # Скачиваем изображение по указанному адресу.
        # использует Python-пакет urllib, чтобы скачать файл картинки
        # Открывает URL-адрес и читает ответ данные, Возвращаемое значение: объект Response.
        # Функция urllib.request.urlopen всегда возвращает объект, который может работать как менеджер контекста
        # и имеет свойства url, заголовки и статус.
        response = request.urlopen(image_url)

        # Любой файл, File связанный с объектом, также имеет несколько дополнительных методов:
        #
        # File.save( имя , содержание , сохранить = Истина ) ¶
        # Сохраняет новый файл с указанным именем и содержимым. Это не перезапишет существующий файл, но будет
        # создан новый файл, и объект будет обновлен, чтобы указывать на этот файл. Если save равно True ,
        # метод save() модели будет вызван после сохранения файла. То есть эти две строчки:

        # вызывает метод save() поля изображения, передавая в него объект скачанного
        # файла, ContentFile. Также используется аргумент commit=False, чтобы пока
        # не сохранять объект в базу данных;
        image.image.save(image_name, ContentFile(response.read()), save=False)
        # при переопределении метода важно оставить стандартное поведение,
        # поэтому сохраняем объект изображения в базу данных только в том слу-
        # чае, если commit равен True.
        if commit:
            image.save()
        return image


    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        # Пользователи не будут
        # вручную заполнять адрес. Вместо этого мы добавим JavaScript-инструмент для
        # выбора картинки на любом постороннем сайте, а наша форма будет получать
        # URL изображения в качестве параметра. Мы заменили виджет по умолчанию
        # для поля url и используем HiddenInput. Этот виджет формируется как input-
        # элемент с атрибутом type="hidden". Мы сделали это для того, чтобы пользователи не видели поле url.
        widgets = {'url': forms.HiddenInput,}

        def clean_url(self):
            url = self.cleaned_data['url']
            valid_extension = ['jpg', 'jpeg']
            extension = url.rsplit('.', 1).lower()
            if extension not in valid_extension:
                raise forms.ValidationError('The given URL does not match valid image extensions.')
            return url
