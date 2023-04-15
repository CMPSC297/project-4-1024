from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, date

class User(AbstractUser):
    pass


class Post(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writer")
    content = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True)

    def __str__(self): 
        return f"{self.user_name} post {self.content} at {self.post_date} with {self.likes} likes"

    @property
    def like_count(self):
        return self.likes.all().count()



class Friend(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ManyToManyField(User, blank=True, default=None, related_name="my_followers")
    following = models.ManyToManyField(User, blank=True, default=None,  related_name="my_following")

    def __str__(self):
        return f"{self.user_name.id}'s relationship."
    
    @property
    def follower_count(self):
        return self.follower.all().count()
        
    @property
    def following_count(self):
        return self.following.all().count()

# class Likes(models.Model):
#     user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")

#     def __str__(self):
#         return f"{self.user_name.id}' like this post."