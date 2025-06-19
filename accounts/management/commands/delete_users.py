from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Delete all users from the database"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        count, _ = User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} user(s)"))
# docker exec -it <container_name> python manage.py delete_users
