from django.conf import settings
from django.db import models
from django.db.models import Count
from django.urls import reverse
from django.utils.text import slugify


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='images_created')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    # Так же как и ForeignKey, ManyToManyField позволяет указать название атрибута,
    # по которому будут доступны связанные объекты. Этот тип поля предоставля-
    # ет менеджер отношения «многие ко многим», с помощью которого можно об-
    # ращаться к связанным объектам в виде image.users_like.all() или из объекта
    # пользователя user как user.images_liked.all().
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='images_liked')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super(Image, self).save(*args, **kwargs)
