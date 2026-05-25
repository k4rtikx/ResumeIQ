from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class UserProfile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    plan = models.CharField(max_length=20,default="free")

    def __str__(self):
        return self.user.username