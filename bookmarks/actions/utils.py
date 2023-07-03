import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Actions


def create_action(user, verb, target=None):
    """позволяет создавать действия, которые опционально включают целевой объект target"""
    now = timezone.now()  # берется текущее время
    last_minute = now - datetime.timedelta(seconds=60)  # используется для хранения даты/времени
    # давностью одна минута назад
    similar_actions = Actions.objects.filter(user_id=user.id,
                                             verb=verb,
                                             created__gte=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct,
                                                 target_id=target.id)
    if not similar_actions:
        action = Actions(user=user, verb=verb, target=target)
        action.save()
        return True
    return False
