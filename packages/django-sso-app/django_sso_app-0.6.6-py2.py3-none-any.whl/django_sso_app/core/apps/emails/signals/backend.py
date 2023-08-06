import logging

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from ..models import EmailAddress

logger = logging.getLogger('django_sso_app.core.apps.emails.signals')


@receiver(post_save, sender=EmailAddress)
def emailaddress_updated(sender, instance, created, **kwargs):
    if kwargs['raw']:
        # https://github.com/django/django/commit/18a2fb19074ce6789639b62710c279a711dabf97
        return

    if instance.primary and instance.verified:
        # deleting all other user email addresses
        logger.info('Email "{}" primary and verified, deleting other user emails'.format(instance))
        user = instance.user
        user.emailaddress_set.exclude(pk=instance.pk).all().delete()
