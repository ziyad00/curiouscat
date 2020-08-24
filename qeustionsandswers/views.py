from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from .models import QA
from .forms import QAForms

def sss(request):
    qas = None
    if request.method == 'POST':
        form = QAForms(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            answer = QA(question=question)
            answer.save()
            #send_mail("there is a question", 
            #"you got a new question", 
            #"ziyad.alotaibe@gmail.com",
            #"lelouch0511@gmail.com")
            form = QAForms()


    else:
        form = QAForms()
        qas = QA.objects.all().exclude(answer__exact='')


    return render(request, 'qeustionsandswers/home.html', {'form': form,
                                                            'qas': qas})