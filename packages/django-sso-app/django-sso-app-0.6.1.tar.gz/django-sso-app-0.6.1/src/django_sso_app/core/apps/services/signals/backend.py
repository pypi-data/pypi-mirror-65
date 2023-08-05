import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import Subscription

logger = logging.getLogger('django_sso_app.core.apps.services.signals')


@receiver(post_save, sender=Subscription)
def check_upated_fields(sender, instance, created, **kwargs):
    if kwargs['raw']:
        # https://github.com/django/django/commit/18a2fb19074ce6789639b62710c279a711dabf97
        return

    if created:  # not instance._state.adding:  # if instance.pk:
        logger.info('Subsciption created, doing nothing')
    else:
        subscription = instance
        if subscription.is_unsubscribed or not subscription.is_active:
            logger.info('Subsciption updates profile rev')

            subscription.profile.update_rev(True)
