from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import FolderPermission

class Command(BaseCommand):
    help = 'Initialize folder permissions for users'

    def handle(self, *args, **kwargs):
        user = User.objects.get(username='sam')
        folder_permission = FolderPermission(
            user=user,
            folder_name='СБШ',
            can_view=True,
            can_edit=False
        )
        folder_permission.save()
        self.stdout.write(self.style.SUCCESS('Successfully initialized folder permissions'))
