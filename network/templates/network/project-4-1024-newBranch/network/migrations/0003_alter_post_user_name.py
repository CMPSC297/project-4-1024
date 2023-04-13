# Generated by Django 4.2 on 2023-04-12 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0002_post"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="user_name",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
