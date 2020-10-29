from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator

from .models import User, Post

class NewPostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

def index(request, page_id=1):
    posts = Post.objects.all().order_by('-date_time')
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
            
def update_post(request, post_id):
    user = request.user

    if user.is_anonymous:
        return HttpResponseRedirect('/login')
    
    if request.method == "PUT":
        form = NewPostForm(request.PUT)
        if form.is_valid():
            content = form.cleaned_data["content"]
            try:
                p = Post.objects(filter(author=user, id=post_id)).first()
                p.content = content
                p.save()
            except:
                p = None
                error = "update error"

    return JsonResponse({"message": "Post updated successfully."}, status=200)    

    

    
def profile(request, profile_id=None, page_id=1):
    user = request.user

    # accessing own profile
    if profile_id is None:
        profile_id = user.id

    posts = Post.objects.filter(author=profile_id).order_by('-date_time')
    profile = User.objects.get(id=profile_id)
    p = Paginator(posts,10)
    page = p.page(page_id)
    try:
        follow = Follow.objects(filter(user=user, profile=profile_id)).first()
    except:
        follow = None 
        
    return render(request, "network/profile.html", {
        "page": page,
        "profile_name": profile.username,
        "followers": profile.followers,
        "following": profile.following,
        "user_is_following": follow

    })

