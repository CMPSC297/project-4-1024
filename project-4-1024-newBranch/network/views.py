from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator
import json
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
    #load all posts
    posts = Post.objects.all().order_by("-post_date")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)
    if not request.user.is_authenticated:
        return render(request, "network/index.html", {
            "anonymous": True,
            "posts": posts,
            "posts_of_the_page": posts_of_the_page,
            "likedPosts": None
        })
    return render(request, "network/index.html", {
        "posts": posts,
        "form": NewPostForm(),
        "posts_of_the_page": posts_of_the_page,
        "likedPosts": posts.filter(likes=request.user)
    })

def profile(request, user_id):
    user = User.objects.get(id=user_id)
    try:
        curr_user = Friend.objects.get(user_name=user)
    except curr_user.DoesNotExist:
        return HttpResponseRedirect(reverse(index))

    posts = Post.objects.filter(user_name=user).order_by("-post_date")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)
    follower = curr_user.follower.all()
    following = curr_user.following.all()
    if not request.user.is_authenticated:
        return render(request, "network/profile.html",{
            "posts_of_the_page": posts_of_the_page,
            "posts": posts,
            "username": user.username,
            "userId": user.id,
            "follower_count": curr_user.follower_count,
            "following_count": curr_user.following_count,
            "anonymous": True,
            "myprofile": True,
            "likedPosts": None
        })
    if request.user.id == user_id: #not allow following 
        return render(request, "network/profile.html",{
            "posts_of_the_page": posts_of_the_page,
            "posts": posts,
            "username": user.username,
            "userId": user.id,
            "follower_count": curr_user.follower_count,
            "following_count": curr_user.following_count,
            "myprofile": True,
            "likedPosts": posts.filter(likes=request.user)
        })
    elif request.user in follower:
        return render(request, "network/profile.html", {
        "posts_of_the_page": posts_of_the_page,
        "posts": posts,
        "username": user.username,
        "userId": user.id,
        "follower_count": curr_user.follower_count,
        "following_count": curr_user.following_count,
        "likedPosts": posts.filter(likes=request.user),
        "unfollow": True
    })
    else:
        return render(request, "network/profile.html", {
            "posts_of_the_page": posts_of_the_page,
            "posts": posts,
            "username": user.username,
            "userId": user.id,
            "follower_count": curr_user.follower_count,
            "following_count": curr_user.following_count,
            "likedPosts": posts.filter(likes=request.user)
        })

def following(request):
    user = request.user
    try:
        curr_user = Friend.objects.get(user_name=user)
    except curr_user.DoesNotExist:
        return HttpResponseRedirect(reverse(index))
    following = curr_user.following.all()
    posts = Post.objects.filter(user_name__in=following).order_by("-post_date")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "posts": posts,
        "likedPosts": posts.filter(likes=request.user),
        "posts_of_the_page": posts_of_the_page

    })

#add or remove like
def like(request, postId):
    post = Post.objects.get(pk=postId)
    if request.user in post.likes.all():
        liked = False
        post.likes.remove(request.user)
    else:
        liked = True
        post.likes.add(request.user)
    return JsonResponse({'liked': liked, 'count' : post.like_count})

def edit(request, postId):
    post = Post.objects.get(pk=postId)
    print("save")
    if request.method == "POST":
        new_content = json.loads(request.body)
        post_content = new_content["new_content"]
        #delete the old post
        Post.objects.filter(pk=postId).delete()
        #add the new post instead of insert
        newpost = Post.objects.create(content=post_content, user_name=request.user)
        return JsonResponse({
            "content": newpost.content,
            "date": newpost.post_date.strftime("%Y-%m-%d %H:%M:%S")
        })
    return JsonResponse({"error": f"Can't edit the post"})

def handle_follow(request, userId):
    user = User.objects.get(id=userId)
    profile_user = Friend.objects.get(user_name=user)
    curr_user = Friend.objects.get(user_name=request.user)
    if request.user in profile_user.follower.all(): #unfollow the profile_user
        followed = True
        profile_user.follower.remove(request.user)
        curr_user.following.remove(user)
    else:
        followed = False
        profile_user.follower.add(request.user)
        curr_user.following.add(user)
    return JsonResponse({'followed': followed, 'followers_count' : profile_user.follower_count, 'following_count' : profile_user.following_count})
        


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
