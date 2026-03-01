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
    path('house/members<int:house_id>',views.members, name='members'),
    path('house/cleaning<int:house_id>',views.cleaning, name='cleaning'),
    path('house/extras<int:house_id>',views.extras, name='extras'),
    path('house/groceries<int:house_id>',views.groceries, name='groceries'),
    path('house/plans<int:house_id>',views.house, name='plans'),
]