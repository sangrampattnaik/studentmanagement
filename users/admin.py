from django.contrib import admin

from .models import Person, Student, Teacher

# Register your models here.



@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["username", "full_name", "email"]
    list_filter = ["is_teacher", "is_student"]

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def username(self, obj):
        return f"{obj.user.username}"

    def email(self, obj):
        return f"{obj.user.email}"


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ["username", "full_name", "email"]

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def username(self, obj):
        return f"{obj.user.username}"

    def email(self, obj):
        return f"{obj.user.email}"


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["username", "full_name", "email", "roll_number"]

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def username(self, obj):
        return f"{obj.user.username}"

    def email(self, obj):
        return f"{obj.user.email}"
