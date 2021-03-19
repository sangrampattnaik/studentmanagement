import re
import sys
from getpass import getpass

import django
from django.core.management.base import BaseCommand

from users.backend import app
from users.models import Person, User


def validate_password(password):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
    mat = re.fullmatch(reg, password)
    
    if mat:
        return True
    return False

class Command(BaseCommand):
    help = "Create Super Admin"
    def handle(self,*args,**kwargs):
        try:
            username = input("Enter username: ")
            while username == "":
                self.stdout.write(self.style.ERROR("username should not be blank"))
                username = input("Enter username: ")
            while User.objects.filter(username=username).exists():
                self.stdout.write(self.style.ERROR("username already taken"))
                username = input("Enter username: ")
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")
            error,msg = app.email_validation(email)
            while not error:
                self.stdout.write(self.style.ERROR(msg))
                email = input("Enter email again: ")
                error,msg = app.email_validation(email)
            while True:
                self.stdout.write(self.style.WARNING("Password shoud contain at least 8 characters and maximum 20 charcater and should have minimum 1 special,uppercase,lowercase, digit character"))
                password = getpass("Enter password: ")
                if validate_password(password):
                    break

            cpassword = getpass("Confirm password: ")
            while password != cpassword:
                self.stdout.write(self.style.ERROR('password does not match'))
                cpassword = getpass("Confirm password: ")
            user = User.objects.create_superuser(username=username,password=password,first_name=first_name,last_name=last_name,email=email)
            Person(user=user,is_superuser=True).save()
            self.stdout.write(self.style.SUCCESS("super admin created successfully"))
        except django.db.utils.OperationalError:
            self.stdout.write(
                self.style.ERROR(
                    'error - No tables found. run command "make migrate" or "python manage.py makemigrations" and "python manage.py migrate"'
                )
            )