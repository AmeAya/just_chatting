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


def create_post(request):
    if not request.user.is_authenticated:
        return redirect(login_view)

    if request.method == 'GET':
        return render(request, 'create_post.html')
    elif request.method == 'POST':
        title = request.POST.get('post_title')
        text = request.POST.get('post_text')
        image = request.FILES.get('post_image')
        post = Post(title=title,
                    text=text,
                    author=request.user,
                    image=image)
        # Создаем Post как объект(ООП)
        post.save()  # Переводит объект в SQL
        return redirect(main_view)


def profile(request):
    if not request.user.is_authenticated:
        return redirect(login_view)

    from django.http import HttpResponse
    try:
        data = {
            'email': request.user.email,
            'name': request.user.name,
            'surname': request.user.surname,
            'photo': request.user.photo.url  # Возвращаем путь к файлу
        }
    except ValueError:
        data = {
            'email': request.user.email,
            'name': request.user.name,
            'surname': request.user.surname
        }
    return HttpResponse(str(data), content_type='application/json', status=200)


# 1) Создать вью user_posts
# 2) Если юзер не авторизован, то перебрасывать на страницу логина
# 3) Иначе, из базы достать все посты где author=request.user
#    posts = Post.objects.filter(author=request.user)
# 4) "Завернуть" все полученные посты в List и отправить их HttpResponse

def user_posts(request):
    if not request.user.is_authenticated:
        return redirect(login_view)

    posts = Post.objects.filter(author=request.user)
    data = []
    for post in posts:
        try:
            data.append({
                'id': post.id,
                'title': post.title,
                'text': post.text,
                'image': post.image.url
            })
        except ValueError:
            data.append({
                'id': post.id,
                'title': post.title,
                'text': post.text
            })
    from django.http import HttpResponse
    import json
    # json.dumps -> Конвертируем из list/dict в нормальный json стринг
    return HttpResponse(json.dumps(data), content_type='application/json', status=200)
