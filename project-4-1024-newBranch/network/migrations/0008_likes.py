# Generated by Django 4.2 on 2023-04-13 00:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0007_alter_friend_follower_alter_friend_following"),
    ]

    operations = [
        migrations.CreateModel(
            name="Likes",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="post_likes",
                        to="network.post",
                    ),
                ),
                (
                    "user_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_likes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]