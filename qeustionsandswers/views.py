from django.shortcuts import render, redirect,get_object_or_404
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from QA.models import QA
from .forms import QAForms, ReplyForms
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from actions.utils import create_action
import redis
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, \
                                  PageNotAnInteger


# connect to redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


    


@login_required
def new_questions(request):
    qas = QA.objects.all().filter(reciever=request.user,published=False)
    paginator = Paginator(qas, 10)
    page = request.GET.get('page')
    try:
        qas  = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        qas = paginator.page(1)
    except EmptyPage:

        if request.is_ajax():

            # If the request is AJAX and the page is out of range
            # return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        qas = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = ReplyForms(request.POST)
        if form.is_valid():
            r_id = form.cleaned_data['r_id']
            question = get_object_or_404(QA, id=r_id)
            new_question = form.save(commit=False)
            new_question.user = request.user
            new_question.qa = question
            new_question.save()
            question.published = True
            question.save()
            create_action(request.user, 'answered', question)
            r.zincrby('questions_ranking', 1, question.id)

            form = ReplyForms()
    else:
        form = ReplyForms()
    if request.is_ajax():
            return render(request, 'qeustionsandswers/list_ajax.html', {'form': form, 'qas':qas})

    return render(request, 'qeustionsandswers/new_questions.html', {'form': form, 'qas':qas})


@login_required
def image_ranking(request):
    # get image ranking dictionary
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # get most viewed images
    most_viewed = list(Image.objects.filter(
                           id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(request,
                  'images/image/ranking.html',
                  {'section': 'images',
                   'most_viewed': most_viewed})