from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'qeustionsandswers'

urlpatterns = [
    path('', views.home, name='home'),
    path('detail/<int:id>/', views.question_detail, name='question_detail'),



]