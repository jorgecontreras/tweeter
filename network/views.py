import json
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follow

class NewPostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

def index(request, page_id=1):
    posts = Post.objects.all().order_by('-updated')
    p = Paginator(posts,10)
    page = p.page(page_id)

    return render(request, "network/index.html", {
        "form": NewPostForm(),
        "page": page
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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def create_post(request):
    user = request.user

    if user.is_anonymous:
        return HttpResponseRedirect('/login')

    if request.method == "POST":
        print("will process now")
        form = NewPostForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            #will save post here
            p = Post(content=content, author=user)
            p.save()
            print("saved post")
            
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "", {
                "form": form
            })
    return render(request, "", {
        "form": NewPostForm()
    })

@csrf_exempt
@login_required        
def update_post(request, post_id):
    
    print("will try to update post" + str(post_id))

    user = request.user
    
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    content = data.get("content")
    
    try:
        p = Post.objects.filter(author=user, id=post_id).first()
        p.content = content
        p.save()
    except:
        p = None
        return JsonResponse({"message": "Error updating the post"}, status=500)

    return JsonResponse({
        "status": "success",
        "content": content,
        "updated": p.updated,
        "id": p.id
        }, status=200)    

def profile(request, profile_id=None, page_id=1):
    user = request.user

    # accessing own profile
    if profile_id is None:
        profile_id = user.id

    posts = Post.objects.filter(author=profile_id).order_by('-updated')
    profile = User.objects.get(id=profile_id)
    p = Paginator(posts,10)
    page = p.page(page_id)
    try:
        follow = Follow.objects.filter(user=user, profile=profile_id).first()
        followers = Follow.objects.filter(profile=profile_id).count()
        following = Follow.objects.filter(user=profile_id).count()
    except:
        follow = None
        followers = 0
        following = 0

    if follow is None:
        follow_button = "Follow"
    else:
        follow_button = "Unfollow"
        
    return render(request, "network/profile.html", {
        "page": page,
        "profile_name": profile.username,
        "followers": followers,
        "following": following,
        "profile_id" : profile.id,
        "follow_button": follow_button

    })

@csrf_exempt
@login_required  
def follow(request, profile_id=None):
    user = request.user

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    profile = User.objects.filter(id=profile_id).first()
    user = User.objects.filter(id=user.id).first()

    if user == profile:
        return JsonResponse({
            "status": "error",
            "following": False
        }, status=200)

    try:
        follow = Follow.objects.filter(user=user, profile=profile).first()
    except:
        follow = None 
        
    # There is no follow, add it
    if follow is None:
        try:
            follow = Follow(user=user, profile=profile)
            follow.save()
            following = True
        except:
            following = False

    # There is a follow, delete it
    else:
        follow.delete()
        following = False

    return JsonResponse({
        "status": "success",
        "following": following
        }, status=200)