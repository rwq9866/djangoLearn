from django.db import models


# Create your models here.

class UserInfo(models.Model):
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)


class Pc(models.Model):
    id = models.UUIDField(primary_key=True, default=None)
    tit = models.CharField(max_length=100)
    hre = models.CharField(max_length=200)
