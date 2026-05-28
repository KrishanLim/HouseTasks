from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class House(models.Model):
    housename = models.CharField(max_length=100)
    members=models.ManyToManyField(User,related_name='house_members')       #House members
    request=models.ManyToManyField(User,related_name='house_request')       #People who sent req to join

    def __str__(self):
        return f'{self.id}-{self.housename}'


class Cleaning_Task(models.Model):
    user_added=models.CharField(max_length=100,blank=True)     #User who added the task
    name = models.CharField(max_length=250, default=None)         #Name of task
    description = models.CharField(max_length=10000, default= None
    )     #Description of task
    date = models.DateTimeField(default=datetime.now, null=True)   #date added
    start_week=models.IntegerField(null=True)        #Week started
    assigned_members = models.ManyToManyField(User)   #Members assigned to the task
    done = models.BooleanField(default=False)       #Done status
    House = models.IntegerField(null=True)     #Links to the House

    def __str__(self):
        return self.name
