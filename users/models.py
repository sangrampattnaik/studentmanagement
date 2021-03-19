from django.db import models
from django.contrib.auth.models import User

class StudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_student=True)

class TeacherManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_teacher=True)


class Person(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='person_user')
    roll_number = models.PositiveIntegerField(blank=True,null=True)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'All User'
    
    @classmethod
    def create_student(cls,**kwargs):
        user = User.objects.create_user(username=kwargs['username'],password=kwargs['password'],first_name=kwargs['first_name'],last_name=kwargs['last_name'],email=kwargs['email'])
        return Cls.objects.create(user=user,is_student=True,roll_number=kwargs['roll_number'])

    @classmethod
    def create_teacher(cls,**kwargs):
        user = User.objects.create_user(username=kwargs['username'],password=kwargs['password'],first_name=kwargs['first_name'],last_name=kwargs['last_name'],email=kwargs['email'])
        return cls.objects.create(user=user,is_teacher=True)





class Teacher(Person):
    objects = TeacherManager()
    class Meta:
        proxy = True

class Student(Person):
    objects = StudentManager()
    class Meta:
        proxy = True