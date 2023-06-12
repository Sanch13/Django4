from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,  # get_user_model()
                                on_delete=models.CASCADE)
    # settings.AUTH_USER_MODEL: Это конфигурационная переменная Django, которая представляет
    # модель пользователя, определенную в проекте. Вместо прямого указания имени
    # модели пользователя, мы используем эту переменную для обеспечения гибкости и совместимости.
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="user/%Y/%m/%d/", blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
