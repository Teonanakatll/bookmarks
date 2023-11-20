from django.contrib.auth.models import User
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


# В предыдущей главе мы добавили отношение «многие ко многим» с помощью
# поля модели ManyToManyField, и Django создал для него таблицу. Это подходит
# для большинства случаев, но иногда необходимо явно задать промежуточную
# модель. Например, это может быть полезно, когда необходимо сохранить до-
# полнительную информацию об отношении (например, когда оно было созда-
# но) или некоторые поля, поясняющие суть отношения.
# Мы добавим такую промежуточную модель. Есть две причины, объясняю-
# щие необходимость этого в нашем проекте:
# мы используем стандартную модель пользователя User из Django и не мо-
# жем ее модифицировать;
# мы хотим сохранить время создания отношения.


class Contact(models.Model):
    # ForeignKey на пользователя подписчика
    user_from = models.ForeignKey('auth.User', related_name='rel_from_set', on_delete=models.CASCADE)
    # ForeignKey на пользователя, на которого подписались
    user_to = models.ForeignKey('auth.User', related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.user_form} follows {self.user_to}"

# Здесь мы обращаемся к методу модели add_to_class(), чтобы с легкостью
# изменить ее. Стоит отметить, что такой способ добавления атрибута реко-
# мендуется использовать только в особенных случаях. Здесь это оправданно,
# т. к. мы:
# упростили доступ к связанным объектам c помощью Django ORM – user.
# followers.all() и user.following.all(). Добавили промежуточную модель
# Contact и избежали лишних объединений таблиц в базе данных, как это
# было бы, если бы мы определили связь в модели Profile;
#  создали таблицу для связи из модели Contact. Таким образом, динамиче-
# ски добавленное в модель User поле ManyToManyField никак не повлияет на
# таблицу пользователей;
#  избежали создания собственной модели пользователя, оставив стан-
# дартную модель User и все ее возможности

User.add_to_class('following',
                  models.ManyToManyField('self', through=Contact,
                                         related_name='followers',
                                         symmetrical=False))
