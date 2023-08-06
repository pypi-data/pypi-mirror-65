from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

from allauth.account.adapter import get_adapter

User = get_user_model()


class Command(BaseCommand):
    help = 'Deletes all user devices (and jwts if APIGATEWAY_ENABLED)'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=str)

    def handle(self, *args, **options):
        usernames = options['username']
        users_count = len(usernames)
        updated_users = 0
        devices_count = 0
        deleted_devices = 0
        parsed_users = 0

        for username in usernames:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR('User "{}" does not exist'.format(username)))
                continue

            adapter = get_adapter()
            profile_devices_count = user.sso_app_profile.devices.count()
            devices_count += profile_devices_count
            deleted_profile_devices_count = adapter.remove_all_user_profile_devices(user)

            if deleted_profile_devices_count > 0:
                deleted_devices += deleted_profile_devices_count
                updated_users += 1

                self.stdout.write(
                    self.style.SUCCESS('Deleted {}/{} profile devices for "{}"'.format(profile_devices_count,
                                                                                       deleted_profile_devices_count,
                                                                                       user)))
            parsed_users += 1
            self.stdout.write(self.style.SUCCESS('{}/{}'.format(parsed_users, users_count)))

        self.stdout.write(self.style.SUCCESS('Updated {}/{} users'.format(updated_users, users_count)))
        self.stdout.write(self.style.SUCCESS('Deleted {}/{} devices'.format(deleted_devices, devices_count)))
