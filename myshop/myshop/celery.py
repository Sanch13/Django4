import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myshop.settings")
app = Celery("myshop")  # создается экземпляр приложения
app.config_from_object("django.conf:settings", namespace="CELERY")  # загружается конфигурация из настроек проекта
# Задав именное пространство CELERY, все настройки Celery должны включать в свое имя префикс
# CELERY_ (например, CELERY_BROKER_URL)
app.autodiscover_tasks()  # Celery будет искать файл tasks.py в каждом каталоге приложений,
# добавленных в INSTALLED_APPS, чтобы загружать определенные в нем асинхронные задания.
