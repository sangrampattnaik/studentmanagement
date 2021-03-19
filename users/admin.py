from django.contrib import admin

# Register your models here.

from .models import Person,Teacher,Student

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["full_name","roll_number","user","user","user",'email']
    list_filter = ['is_teacher','is_student']

    def full_name(self,obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def username(self,obj):
        return f"{obj.user.username}"
    def email(self,obj):
        return f"{obj.user.email}"



@admin.register(Teacher)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["user","is_teacher","user","user",]

@admin.register(Student)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["user","is_teacher","user","user"]