from django.shortcuts import render, redirect,get_object_or_404
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from QA.models import QA
from .forms import QAForms, ReplyForms
from django.contrib.auth import get_user_model


def home(request):
    qas = QA.objects.all().filter(published=True)
    if request.method == 'POST':
        form = QAForms(request.POST)
        if form.is_valid():
            new_question = form.save()
            new_question.save()
            form = QAForms()

            

    else:
        form = QAForms()
    return render(request, 'qeustionsandswers/home.html', {'form': form, 'qas':qas})

def question_detail(request, id):
    
    question = get_object_or_404(QA, id=id)
    User = get_user_model()
    deafult_user = User.objects.get(id=2)
    if request.method == 'POST':
        form = ReplyForms(request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            if request.user.is_authenticated:
                new_reply.user = request.user
            else:
                new_reply.user = deafult_user

            new_reply.qa = question

            new_reply.save()

            form = ReplyForms()

    else:
        form = ReplyForms()
    # increment image ranking by 1
    #r.zincrby('image_ranking', 1, image.id)
    return render(request,
                  'qeustionsandswers/detail.html',
                  {'qa': question,
                  'form': form})



