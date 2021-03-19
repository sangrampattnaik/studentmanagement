import os

import django
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from users.models import Person

class Command(BaseCommand):
    help = "create superuser username = admin and password = admin"

    def handle(self, *args, **kwargs):
        try:
            if User.objects.filter(username="admin").exists():
                self.stdout.write(self.style.ERROR("already admin superuser created"))
                quit()
            else:
                user = User.objects.create_superuser(username="admin", password="admin")
                Person.objects.create(is_superuser=true,user=user)
                self.stdout.write(
                    self.style.SUCCESS(
                        'super user "admin" created and password = "admin"'
                    )
                )
        except django.db.utils.OperationalError:
            self.stdout.write(
                self.style.ERROR(
                    'error - No tables found. run command "make migrate" or "python manage.py makemigrations" and "python manage.py migrate"'
                )
            )
