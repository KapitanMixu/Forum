from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    desc = models.CharField(max_length=1000)
    ROLES = (
        ('R', 'Redaktor'),
        ('C', 'Czytelnik')
    )
    role = models.CharField(max_length=10, choices=ROLES)

    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length=40)
    pub_date = models.DateTimeField(auto_now_add=True)
    main_text = models.CharField(max_length=4000)
    author = models.ForeignKey(UserProfile, default=None, on_delete=models.CASCADE)
    rate = models.FloatField(default=0)
    rate_number = models.IntegerField(default=0)
    tags = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.title


class Comment(models.Model):
    main_post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, default=None, related_name='comment', on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=1000)
    pub_date = models.DateTimeField(auto_now_add=True)

