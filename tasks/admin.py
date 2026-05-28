from django.contrib import admin
from .models import House, Cleaning_Task

# Register your models here.
admin.site.register(House),
admin.site.register(Cleaning_Task)