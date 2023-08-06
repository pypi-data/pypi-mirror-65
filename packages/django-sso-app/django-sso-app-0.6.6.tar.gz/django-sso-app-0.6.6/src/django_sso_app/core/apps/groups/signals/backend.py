import logging

from django.contrib.auth.models import Group as GroupModel
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from ....permissions import is_staff
from ..models import Group
from ...profiles.models import Profile

logger = logging.getLogger('django_sso_app.core.apps.groups.signals')


@receiver(m2m_changed)
def signal_handler_when_user_is_added_or_removed_from_group(action, instance, pk_set, model, **kwargs):
    if model == Group and instance.__class__ == Profile:
        user = instance.user
        profile = instance

        if not user.is_superuser:
            logger.info('Groups signal')

            is_loaddata = getattr(profile, '__django_sso_app__loaddata', False)
            is_creating = getattr(user, '__django_sso_app__creating', False)

            must_update_rev = (not is_loaddata) and (not is_creating)

            groups_updated = False

            if action == 'pre_add':
                groups_updated = True
                for pk in pk_set:
                    _group = Group.objects.get(id=pk)
                    logger.info('Profile "{}" entered group "{}"'.format(profile, _group))

            elif action == 'pre_remove':
                groups_updated = True
                for pk in pk_set:
                    _group = Group.objects.get(id=pk)
                    logger.info('Profile "{}" exited from group "{}"'.format(profile, _group))

            # updating rev

            if groups_updated and must_update_rev:
                profile.update_rev(True)
