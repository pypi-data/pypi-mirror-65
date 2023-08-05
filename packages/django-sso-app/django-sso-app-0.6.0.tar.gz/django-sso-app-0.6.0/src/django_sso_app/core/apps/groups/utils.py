import logging

# import pyximport
# pyximport.install()

from ...functions import lists_differs

logger = logging.getLogger('django_sso_app.core.apps.groups')


def update_profile_groups(profile, groups_list):
    previous_groups_list = list(profile.groups.order_by('name').values_list('name', flat=True))

    if lists_differs(previous_groups_list, groups_list):
        logger.info('groups updated for "{}"'.format(profile))

        for group_name in groups_list:
            profile.add_to_group(group_name)
