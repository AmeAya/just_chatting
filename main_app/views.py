from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import *


def main_view(request):
    if request.user.is_authenticated:
        # request.user -> Юзер
        following_users = request.user.following.all()

        posts = []
        for user in following_users:
            user_posts = Post.objects.filter(author=user)
            for post in user_posts:
                posts.append(post)

        context = {
            'posts': posts
        }
        return render(request, 'main.html', context=context)
    else:
        return redirect(login_view)


def login_view(request):
    if request.user.is_authenticated:
        return redirect(main_view)

    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            context = {
                'message': 'Login and/or password is invalid!'
            }
            return render(request, 'login.html', context=context)
        else:
            login(request, user)
            return redirect(main_view)


# 1) Создать вью create_post.
#    На GET нужно возвращать html страницу
#    На POST принять с html два поля(title, text)
# 2) Создать html страницу для create_post(extends 'base.html')
# 3) На html странице создать form с методом post.
#    В формочке создать два инпута(title, text), label к ним, submit кнопку
