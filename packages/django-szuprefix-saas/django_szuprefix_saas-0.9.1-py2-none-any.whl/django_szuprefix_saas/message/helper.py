# -*- coding:utf-8 -*- 
__author__ = 'denishuang'
from . import models
from django.contrib.auth.models import User
from ..saas.helper import get_default_party


def send_message(sender, receivers, title, content=None, is_force=False, unique_id=None):
    if not isinstance(receivers, (list, tuple, set)):
        receivers = [receivers]
    party = sender.as_saas_worker.party if hasattr(sender, 'as_saas_worker') else get_default_party()
    for r in receivers:
        user = r if isinstance(r, User) else r.user
        if unique_id:
            models.Message.objects.update_or_create(
                party=party,
                receiver=user,
                unique_id=unique_id,
                defaults=dict(
                    sender=sender,
                    title=title,
                    is_read=False,
                    is_force=is_force
                )
            )
        else:
            models.Message.objects.create(
                party=party,
                sender=sender,
                receiver=user,
                title=title,
                is_read=False,
                is_force=is_force
            )

def revoke_message(receiver, unique_id):
    if not unique_id:
        raise Exception("unique_id can not be empty")
    models.Message.objects.filter(receiver=receiver, unique_id=unique_id, is_read=False).delete()