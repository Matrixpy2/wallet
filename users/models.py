from django.db import models
from  django.contrib.auth.models import AbstractUser , Group , Permission
from django.db.models import ForeignKey, CASCADE


# Create your models here.


class customer(AbstractUser):
    fullName=models.CharField(max_length=255)
    number_id = models.CharField(max_length=10 , unique=True)


    def __str__(self):
        return f'{self.fullName} '
