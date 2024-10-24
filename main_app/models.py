from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if email is None:
            raise ValueError('Email is required!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    photo = models.ImageField(null=True, blank=True, upload_to='users')
    # upload_to -> Куда сохранить картинку внутри папки медиа

    followers = models.ManyToManyField('CustomUser', blank=True, related_name='many_to_many_followers')
    following = models.ManyToManyField('CustomUser', blank=True, related_name='many_to_many_following')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='posts')
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    like_counter = models.PositiveIntegerField(default=0)
    dislike_counter = models.PositiveIntegerField(default=0)


class Comment(models.Model):
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='posts')
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    like_counter = models.PositiveIntegerField(default=0)
    dislike_counter = models.PositiveIntegerField(default=0)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
