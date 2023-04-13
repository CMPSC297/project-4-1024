from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, date

class User(AbstractUser):
    pass


class Post(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writer")
    content = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self): 
        return f"{self.user_name} post {self.content} at {self.post_date} with {self.likes} likes"

class Friend(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ManyToManyField(User, blank=True, default=None, related_name="my_followers")
    following = models.ManyToManyField(User, blank=True, default=None,  related_name="my_following")

    def __str__(self):
        return f"{self.user_name.id}'s relationship."

class Likes(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")

    def __str__(self):
        return f"{self.user_name.id}' like this post."