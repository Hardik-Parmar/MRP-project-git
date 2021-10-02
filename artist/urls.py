from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path('', views.artistHome, name='home'),
    path('', views.artistHomeWithOutLogin, name='statichome'),
    path('home/', views.ClubChartView.as_view(), name='home'),
    path('documents/', views.viewDocuments, name='documents'),
    path('login/', views.handleLogin, name='login'),
    path('logout/', views.handleLogout, name='logout'),
]