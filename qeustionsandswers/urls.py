from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'qeustionsandswers'

urlpatterns = [
    #path('detail/<int:id>/', views.question_detail, name='question_detail'),
    path('new/', views.new_questions, name='new_questions'),

   # path('new/<int:id>', views.new_questions, name='new_questions_ids'),



]