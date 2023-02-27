from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
# Create your models here.

class UserAccount(AbstractUser):
    username = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=35)
    profile_picture = models.FileField(null=True)
    bio = models.TextField(max_length=255)
    close_friends = models.ManyToManyField('self', symmetrical=False, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'bio']

    def __str__(self):
        return self.username
