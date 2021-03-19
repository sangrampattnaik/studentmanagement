from rest_framework import serializers

from .models import Person


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["id", "full_name", "username", "email", "is_teacher"]


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["id", "full_name", "username", "email",'roll_number', "is_student"]
