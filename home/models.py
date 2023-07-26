from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



# class User(AbstractUser):
#     username = models.CharField(max_length=200, blank=True, null=True, unique=True)
#     name = models.CharField(max_length=200)
#     email = models.CharField(max_length=200, unique=True)
#     password = models.CharField(max_length=200)


#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.username



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    password2 = models.CharField(max_length=200)  # New field 'password2'


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Add any required fields here if needed

    def __str__(self):
        return self.email



class DocterModel(models.Model):
    name = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    age = models.IntegerField()
    spec = models.CharField(max_length=200)
    email = models.EmailField(unique=True,null=True)
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.name