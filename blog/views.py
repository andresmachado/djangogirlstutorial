from django.http import *
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
from .forms import PostForm, UserCreateForm
from .models import Post


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('blog.views.post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})
    else:
        return redirect('login_user')

def post_edit(request, pk):
    if request.user.is_authenticated():
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('blog.views.post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
    else:
        return redirect('login_user')

def login_user(request):
    # logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
    return render_to_response('blog/login.html', context_instance=RequestContext(request))

def logout_user(request):
    if request.user.is_authenticated():
        logout(request)
        return render(request, 'blog/login.html')
    else:
        return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('registration_complete'))
    else:
        form = UserCreateForm()
    token = {}
    token.update(csrf(request))
    token['form'] = UserCreateForm()

    return render_to_response('blog/signup.html', token)

def registration_complete(request):
    return render_to_response('blog/registration_complete.html')

@login_required
def user_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.user.id == pk:
        return render(request, 'blog/user_profile.html', {'user': user})
    else:
        return render(request, 'blog/user_profile.html')
