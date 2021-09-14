from django.contrib.auth.models import User
from django.http import request
from insta.models import Profile, Image, Comment
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, commentForm, profileForm, userForm, postImageForm
# Create your views here.


@login_required(login_url='/accounts/login/')
def index(request):
    profile = Profile.objects.all()
    posts = Image.objects.all()

    return render(request, 'index.html', {"profile": profile, "posts": posts})


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():

            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
        return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration_form.html', {"form": form})


@login_required(login_url='/accounts/login/')
def profile(request):

    if request.method == 'POST':
        user_form = userForm(request.POST, instance=request.user)
        profile_form = profileForm(
            request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('index')
    else:
        profile_form = profileForm(instance=request.user)
        user_form = userForm(instance=request.user)
    return render(request, 'user_profile.html', {"user_form": user_form, "profile_form": profile_form})


def searchprofile(request):
    if 'insta' in request.GET and request.GET['insta']:
        name = request.GET.get("insta")
        searchResults = Profile.search_profile(name)
        message = f'name'
        params = {
            'results': searchResults,
            'message': message
        }
        return render(request, 'search.html', params)
    else:
        message = "You haven't searched for any image category"
    return render(request, 'search.html', {'message': message})


def post_image(request):
    profile = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = postImageForm(request.POST, request.FILES)
        if form.is_valid():
            ig_post = form.save(commit=False)
            ig_post.profile = request.user.profile
            ig_post.save()
            return redirect("index")
    else:
        form = postImageForm()
    return render(request, 'post_image.html', {"form": form})


@login_required(login_url='/accounts/login/')
def update_profile(request):

    if request.method == 'POST':
        user_form1 = userForm(request.POST, instance=request.user)
        profile_form1 = profileForm(
            request.POST, request.FILES, instance=request.user.profile)
        if profile_form1.is_valid() and user_form1.is_valid:

            profile_form1.save()
            user_form1.save()
            return redirect('profile')

    else:
        user_form1 = userForm(instance=request.user)
        profile_form1 = profileForm(instance=request.user.profile)

    return render(request, 'update_profile.html', {"user_form1": user_form1, "profile_form1": profile_form1})


@login_required(login_url='accounts/login/')
def comment(request, image_id):
    current_user = request.user
    images = Image.objects.get(id=image_id)
    user_profile = Profile.objects.get(username=current_user)
    comments = Comment.objects.all()

    if request.method == 'POST':
        form = commentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image_post = images
            comment.comment_by = user_profile
            comment.save()
        return redirect('index')
    else:
        form = commentForm()
    return render(request, 'comment.html', {"form": form, "images": images, 'comments': comments})
