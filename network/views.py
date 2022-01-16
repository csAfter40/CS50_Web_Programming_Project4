from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required

from .models import User, Post, Like, Follow


def index(request, username = None):
    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
            text = request.POST["text"]
            post = Post(user=user, text=text)
            post.save()
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "network/login.html")
    
    if request.method == "PUT":
        if request.user.is_authenticated:
            data = json.loads(request.body)
            user = request.user
            post_id = data["id"]
            post = Post.objects.get(id=post_id)
            if user == post.user:
                return JsonResponse({}, status=400)
            try:
                like = Like(user=user, post=post)
                like.save()
            except IntegrityError:
                like = Like.objects.get(user=user, post=post)
                like.delete()
            count = post.like_set.all().count()
            return JsonResponse({"id": post_id, "count": count}, status=200)
        else:
            return JsonResponse({}, status=400)
    view_user = None
    follow = None
    if username:
        view_user = User.objects.get(username=username)
        posts = Post.objects.filter(user=view_user).order_by("-time_stamp")
        try: 
            follow = Follow.objects.get(follower=request.user, following=view_user)
        except Follow.DoesNotExist:
            follow = None
    else:
        posts = Post.objects.all().order_by("-time_stamp")
    context = {
            "posts": posts,
            "view_user": view_user,
            "follow": follow
        }
    if request.user.is_authenticated:
        likes = request.user.like_set.all()
        liked_posts = [like.post for like in likes]
        context["liked_posts"] = liked_posts
    return render(request, "network/index.html", context)
    
# @login_required(login_url=reverse('login'))
def follow(request, username):
    if request.method == "PUT":
        follower_user = request.user
        following_user = User.objects.get(username=username)
        if following_user == follower_user:
            return JsonResponse({}, status=400)
        try: 
            follow = Follow(follower=follower_user, following=following_user)
            follow.save()
        except IntegrityError:
            follow = Follow.objects.get(follower=follower_user, following=following_user)
            follow.delete()
        return JsonResponse({}, status=200)
        
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
