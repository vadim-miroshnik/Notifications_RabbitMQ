# Generated by Django 4.0.4 on 2023-02-13 13:16

from django.db import migrations, models
from movies.models import User, NotificationGroup, Template


notify_template_example = """Dear {{ user }},
We hope this email finds you well. We kindly ask that you please confirm your email address by replying to this email or clicking the link below.
Thank you for your time and cooperation.
Sincerely, Best Online Cinema Stock
"""


def add_default_data(apps, schema_editor):
    # User = apps.get_model("movies", "User")
    notification_group = NotificationGroup.objects.create(id="9fe7e975-a8e9-4387-9dc3-c92770ffd1cb", name="Common")
    user = User.objects.create(
        fullname="Тестовый пользователь",
        login="test_user",
        password="password",
        email="test@example.com",
        phone="+77770000000",
    )
    user.notification_group.add(notification_group)
    user.save()
    notification_group.save()
    template = Template.objects.create(
        id="7dfba2c1-4057-4ef7-a85d-452aae23d428", name="RegularNotify", template=notify_template_example
    )
    template.save()


def remove_default_data(apps, schema_editor):
    User.objects.all().delete()
    NotificationGroup.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_default_data, remove_default_data),
    ]