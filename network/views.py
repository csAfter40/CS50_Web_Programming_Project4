from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
import json
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from sympy import re
from django.core.paginator import Paginator

from .models import User, Post, Like, Follow


def index(request, username = None, following_page=False):
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
        page_title = None
        try: 
            follow = Follow.objects.get(follower=request.user, following=view_user)
        except Follow.DoesNotExist:
            follow = None
    elif following_page:
        following_set = Follow.objects.filter(follower=request.user)
        following_users = [follow_item.following for follow_item in following_set]
        posts = Post.objects.filter(user__in=following_users).order_by("-time_stamp")
        page_title = "Following"
    else:
        posts = Post.objects.all().order_by("-time_stamp")
        page_title = "All posts"

        # Pagination code
    posts_per_page = 10
    post_paginator = Paginator(posts, posts_per_page)
    page_number = request.GET.get("page", 1)
    page = post_paginator.get_page(page_number)
    context = {
            "page": page,
            "view_user": view_user,
            "follow": follow,
            "followers": Follow.objects.filter(following=view_user).count(),
            "following": Follow.objects.filter(follower=view_user).count(),
            "page_title": page_title
        }
    if request.user.is_authenticated:
        likes = request.user.like_set.all()
        liked_posts = [like.post for like in likes]
        context["liked_posts"] = liked_posts
    return render(request, "network/index.html", context)

@login_required
def following(request):
    return index(request, following_page=True)

@login_required
def edit(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        print(data)
        id = data.get("id")
        text = data.get("text")
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return JsonResponse({"message": f"Post #{id} not found"}, status=400)
        post.text = text
        post.save()
        return JsonResponse({}, status=200)
        
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
        return JsonResponse({"followers": Follow.objects.filter(following=following_user).count()}, status=200)
        
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            index_url = reverse("index")
            print(request.POST)
            return redirect(request.POST.get("next", index_url))
            # return HttpResponseRedirect(reverse("index"))
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
