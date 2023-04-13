from django.contrib import admin
from .models import Post, Friend

#configure the admin interface
class FlightAdmin(admin.ModelAdmin):
    list_display  = ("user_name", "content", "post_date", "likes")

# Register your models here.
admin.site.register(Post)
admin.site.register(Friend)
