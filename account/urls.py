from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
  
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('users/<username>/', views.user_detail, name='user_detail'),
]
