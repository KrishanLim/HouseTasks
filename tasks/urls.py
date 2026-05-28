from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='index'),
    path('cleaning',views.cleaning,name='cleaning'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('enterhouse',views.enterhouse,name='enterhouse'),
    path('request_join',views.request_join,name='request_join'),
    path('buildhouse/',views.buildhouse, name='buildhouse'),
    path('house/<int:house_id>',views.house, name='house'),
    path('members/<int:house_id>',views.members, name='members'),
    path('cleaning/<int:house_id>',views.cleaning, name='cleaning'),
    path('task_action/<int:house_id>',views.task_action,name='task_action'),
    path('edit_task/<int:house_id>',views.edit_task,name='edit_task')
]