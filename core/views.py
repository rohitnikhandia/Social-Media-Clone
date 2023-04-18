from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from .models import *
from itertools import chain
import random


# Create your views here.
@login_required(login_url="signin")
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(
        follower=request.user.username)
    for users in user_following:
        user_following_list.append(users.user)
    for username in user_following_list:
        feed_lists = Post.objects.filter(user=username)
        feed.append(feed_lists)
    feed_list = list(chain(*feed))

    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(
        all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(
        new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(request, "index.html", {"user_profile": user_profile, "posts": feed_list, "suggestions_username_profile_list": suggestions_username_profile_list[:4]})


def signup(request):

    if request.method == "POST":
        user_data = request.POST
        username = user_data.get("username")
        email = user_data.get("email")
        password = user_data.get("password")
        confirm_password = user_data.get("confirm_password")
        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return redirect("/signup/")
            elif User.objects.filter(username=username).exists():
                messages.info(
                    request, f"A user with username:{username} already exists.")
                return redirect("/signup/")
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()
                messages.info(request, "User Created successfully.")

                user_login = auth.authenticate(
                    username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(
                    user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect("/settings/")

        else:
            messages.info(request, "Passwords did not match")
            return redirect("/signup/")
    return render(request, "signup.html")


def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Invalid Credentials")
            return redirect("signin")
    return render(request, "signin.html")


@login_required(login_url="signin")
def upload(request):
    if request.method == "POST":
        caption = request.POST.get("caption")
        image = request.FILES.get("image_upload")
        user = request.user.username
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect("/")
    return redirect("/")


@login_required(login_url="signin")
def like_post(request, post_id):
    username = request.user.username
    post_id = post_id

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(
        username=username, post_id=post_id).first()

    if like_filter is None:
        new_like = LikePost.objects.create(username=username, post_id=post_id)
        new_like.save()

        post.no_of_likes += 1
        post.save()
        return redirect("/")
    else:
        like_filter.delete()
        post.no_of_likes -= 1
        post.save()
        return redirect("/")


@login_required(login_url="signin")
def follow(request):
    if request.method == "POST":
        follower = request.POST["follower"]
        user = request.POST["user"]
        if FollowersCount.objects.filter(follower=follower, user=user).first() is None:
            follow_object = FollowersCount.objects.create(
                follower=follower, user=user)
            follow_object.save()
            return redirect("/profile/"+user+"/")
        else:
            FollowersCount.objects.get(follower=follower, user=user).delete()
            return redirect("/profile/"+user+"/")
    return redirect()


@login_required(login_url="signin")
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    if request.method == "POST":
        username = request.POST["username"]
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))

    return render(request, "search.html", {"username_profile_list": username_profile_list, "user_object": user_object, "user_profile": user_profile})


@login_required(login_url="signin")
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    profile_object = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)
    user_followers = FollowersCount.objects.filter(user=pk)

    follower = request.user.username
    user = pk
    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = "Unfollow"
    else:
        button_text = "Follow"

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        "user_object": user_object,
        "profile_object": profile_object,
        "user_posts": user_posts,
        "user_post_length": user_post_length,
        "button_text": button_text,
        "user_followers": user_followers,
        "user_following": user_following,
    }

    return render(request, "profile.html", context)


@login_required(login_url="signin")
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        if request.FILES.get("profile_img") is None:
            profile_img = user_profile.profile_img
        elif request.FILES.get("profile_img"):
            profile_img = request.FILES.get("profile_img")

        bio = request.POST.get("bio")
        location = request.POST.get("location")

        user_profile.profile_img = profile_img
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        return redirect("settings")

    return render(request, "setting.html", {"user_profile": user_profile})


@login_required(login_url="signin")
def signout(request):
    auth.logout(request)
    return redirect("signin")
