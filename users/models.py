from django.db import models
from  django.contrib.auth.models import User
from django.db.models import ForeignKey, CASCADE


# Create your models here.


class users(models.Model):
    user=models.OneToOneField(User , on_delete=CASCADE)
    username=models.CharField(max_length=255)
    fullName=models.CharField(max_length=255)
    number_id = models.CharField(max_length=10 , unique=True)
