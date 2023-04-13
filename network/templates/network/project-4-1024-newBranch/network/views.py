from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Post, Friend

#using forms library
class NewPostForm(forms.Form):
    post = forms.CharField(label='', widget=forms.Textarea(attrs={'cols': 80, 'rows': 4})) #client side validation


def index(request):

    if request.method == "POST":
        form = NewPostForm(request.POST)#request.POST contains all data user submitted
        if form.is_valid():
            content = form.cleaned_data["post"]
            #create a new post object and insert to the post db
            Post.objects.create(content=content, user_name=request.user)
            return HttpResponseRedirect(reverse(index))

    posts = Post.objects.all().order_by("-post_date")
    if not request.user.is_authenticated:
        return render(request, "network/index.html", {
            "anonymous": True,
            "posts": posts
        })
    return render(request, "network/index.html", {
        "posts": posts,
        "form": NewPostForm()
    })

def profile(request, user_id):
    user = User.objects.get(id=user_id)
    try:
        curr_user = Friend.objects.get(user_name=user)
    except curr_user.DoesNotExist:
        return HttpResponseRedirect(reverse(index))
    posts = Post.objects.filter(user_name=user).order_by("-post_date")
    follower_count = curr_user.follower.all().count()
    following_count = curr_user.following.all().count()
    if request.user.id == user_id or not request.user.is_authenticated: #not allow following 
        return render(request, "network/profile.html",{
            "posts": posts,
            "username": user.username,
            "follower_count": follower_count,
            "following_count": following_count,
            "myprofile": True
        })
    return render(request, "network/profile.html", {
        "posts": posts,
        "username": user.username,
        "follower_count": follower_count,
        "following_count": following_count
    })

def following(request):
    user = request.user
    try:
        curr_user = Friend.objects.get(user_name=user)
    except curr_user.DoesNotExist:
        return HttpResponseRedirect(reverse(index))
    following = curr_user.following.all()
    posts = Post.objects.filter(user_name__in=following).order_by("-post_date")
    return render(request, "network/following.html", {
        "posts": posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            #create a new Friend object to keep track of user relationship
            Friend.objects.create(user_name=user)
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
