from django.db import models

from django.conf import settings

class Profile(models.Model):
    # Чтобы наш код не зависел от конкретной модели пользователя, мы используем функцию get_user_model().
    # Она возвращает модель, указанную в настройке AUTH_USER_MODEL, и мы можем легко заменять класс пользователя,
    # т. к. не обращались в коде напрямую к конкретной модели.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return f"Profile for user {self.user.username}"
