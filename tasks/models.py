from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class House(models.Model):
    housename = models.CharField(max_length=100)
    members=models.ManyToManyField(User)

    def __str__(self):
        return self.housename


class Cleaning_Task(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    done = models.BooleanField(default=False)
    House = models.IntegerField(blank=True)     #Links to the House

    def __str__(self):
        return self.name
