# Generated by Django 3.0.3 on 2021-03-19 04:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_number', models.PositiveIntegerField(blank=True, null=True)),
                ('is_teacher', models.BooleanField(default=False)),
                ('is_student', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='person_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
