from django.db import models

# Create your models here.
class UserInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    age = models.IntegerField()