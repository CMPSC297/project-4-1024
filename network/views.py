from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User, Post, Follow, Like

def like(request, id):

    try:
        css_class = 'fas fa-heart'
        user = User.objects.get(id=request.session['_auth_user_id'])
        post = Post.objects.get(id=id)
        like = Like.objects.get_or_create(
            user=user, post=post)
        if not like[1]:
            css_class = 'far fa-heart'
            Like.objects.filter(user=user, post=post).delete()

        total_likes = Like.objects.filter(post=post).count()
    except KeyError:
        return HttpResponseBadRequest("Bad Request: no like chosen")
    return JsonResponse({
        "like": id, "css_class": css_class, "total_likes": total_likes
    })


def remove_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    like = Like.objects.filter(user=user, post=post).first()
    if like:
        like.delete()
        return JsonResponse({"message": "Like removed!"})
    return JsonResponse({"message": "No such like exists"})


def add_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    new_like, created = Like.objects.get_or_create(user=user, post=post)
    if created:
        return JsonResponse({"message": "Like added!"})
    return JsonResponse({"message": "You already liked this post"})


def edit(request, post_id):
    if request.method == "POST":
        data = request.POST
        post = get_object_or_404(Post, id=post_id, user=request.user)
        post.content = data["content"]
        post.save()
        return JsonResponse({"message": "Change successful", "data": data["content"]})


def index(request):
    all_posts = Post.objects.all().order_by("-id")
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)
    all_likes = Like.objects.all()
    whoYouLiked = []
    try:
        for like in allLikes:
            if like.user.id == request.user.id:
                whoYouLiked.append(like.post.id)
    except:
        whoYouLiked = []
    return render(request, "network/index.html", {
        "all_posts": all_posts,
        "posts_of_the_page": posts_of_the_page,
        "who_you_liked": whoYouLiked
    })


def newPost(request):
    if request.method == "POST":
        content = request.POST.get('content')
        user = request.user
        post = Post.objects.create(content=content, user=user)
        return HttpResponseRedirect(reverse(index))


def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    all_posts = Post.objects.filter(user=user).order_by("-id")
    following = Follow.objects.filter(user=user)
    followers = Follow.objects.filter(user_follower=user)
    is_following = followers.filter(user=request.user).exists()
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
        "all_posts": all_posts,
        "posts_of_the_page": posts_of_the_page,
        "username": user.username,
        "following": following,
        "followers": followers,
        "is_following": is_following,
        "user_profile": user
    })
    

def following(request):
    following_people = Follow.objects.filter(user=request.user)
    following_posts = Post.objects.filter(user__in=following_people.values('user_follower')).order_by('-id')
    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "posts_of_the_page": posts_of_the_page
    })


def follow(request):
    userfollow = request.POST['userfollow']
    userfollow_data = get_object_or_404(User, username=userfollow)
    Follow.objects.get_or_create(user=request.user, user_follower=userfollow_data)
    return redirect('profile', user_id=userfollow_data.id)


def unfollow(request):
    userfollow = request.POST['userfollow']
    userfollow_data = get_object_or_404(User, username=userfollow)
    Follow.objects.filter(user=request.user, user_follower=userfollow_data).delete()
    return redirect('profile', user_id=userfollow_data.id)

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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")