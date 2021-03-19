from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os
import django

class Command(BaseCommand):
    help = 'create superuser username = admin and password = admin'

    def handle(self, *args, **kwargs):
        try:
            if User.objects.filter(username="admin").exists():
                self.stdout.write(self.style.ERROR('already admin superuser created'))
                quit()
            else:
                User.objects.create_superuser(username="admin",password="admin")
                self.stdout.write(self.style.SUCCESS('super user "admin" created and password = "admin"'))
        except django.db.utils.OperationalError:
            self.stdout.write(self.style.ERROR('error - No tables found. run command "make migrate" or "python manage.py makemigrations" and "python manage.py migrate"'))