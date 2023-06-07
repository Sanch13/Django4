from django.contrib.auth.models import User


class EmailAuthBackend:
    """    Authenticate with email    """

    def authenticate(self, request, username=None, password=None) -> "user":
        """Возвращает user если email есть в БД и password совпадает с введенным"""
        try:
            user = User.objects.get(email=username)
            # извлекается пользователь с данным адресом электронной почты
            if user.check_password(password):
                # check_password() хеширует пароль, чтобы сравнить данный
                # пароль с паролем, хранящимся в базе данных
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            # DoesNotExist возникает, если пользователь с данным email не найден.
            # MultipleObjectsReturned возникает, если найдено несколько пользователей с одним
            # и тем же email
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
