from django.contrib import admin
from django.urls import path
# from home.views import home_view,index
from . import  views

urlpatterns = [
    path('signup',views.signup),
    path('login',views.login),
    path('postrecipe',views.createpost),
    path('logout',views.logout),
    path('checkuser',views.checkuser),
    path('recipe',views.recipe),
    path('userprofile',views.userprofile),
    path('updatepost/<int:id>',views.updatepost),
    path('delete/<int:id>',views.deletepost),
    path('updateprofile',views.updateprofile),
    path('interactions/<int:id>',views.interactions),
    path('notification',views.notification),
    path('topten',views.topten),
    path('follow/<int:id>',views.follow),
    
]