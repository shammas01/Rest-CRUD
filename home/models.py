from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=200, blank=True, null=True, unique=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class DocterModel(models.Model):
    name = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    age = models.IntegerField()
    spec = models.CharField(max_length=200)
    email = models.EmailField(unique=True,null=True)
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.name