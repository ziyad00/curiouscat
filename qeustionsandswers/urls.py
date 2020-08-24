from django.urls import path

from . import views

app_name = 'qeustionsandswers'

urlpatterns = [
    path('', views.sss, name='questions'),

]