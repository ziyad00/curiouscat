from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .models import Profile, Contact
from .forms import LoginForm, UserRegistrationForm, \
                   UserEditForm, ProfileEditForm
from qeustionsandswers.forms import QAForms, ReplyForms
from QA.models import QA
from common.decorators import ajax_required
from actions.utils import create_action
from actions.models import Action
import redis
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, \
                                  PageNotAnInteger

# connect to redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)




def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})



def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    qas = QA.objects.all().filter(reciever=user,published=True)
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
        QA_form = QAForms(request.POST, initial={"form_type": "10"})
        reply_form = ReplyForms(request.POST, initial={"form_type": "10"})

        if request.POST.get("form_type") == 'formOne' and QA_form.is_valid():
            new_question = QA_form.save(commit=False)
            new_question.reciever = user
            new_question.save()
            QA_form = QAForms()
        elif request.POST.get("form_type") == 'formTwo' and reply_form.is_valid():
            r_id = reply_form.cleaned_data['r_id']
            question = get_object_or_404(QA, id=r_id)
            new_question = reply_form.save(commit=False)
            new_question.user = request.user
            new_question.qa = question
            new_question.save()
            question.published = True
            question.save()
            create_action(request.user, 'replied on', question)
            r.zincrby('questions_ranking', 1, question.id)
            reply_form = ReplyForms()

    else:
            QA_form = QAForms()
            reply_form = ReplyForms()
    if request.is_ajax():
            return render(request, 'qeustionsandswers/list_ajax.html', {'form': form, 'qas':qas})
    return render(request,
                  'account/user/detail.html',
                  {'user': user,
                    'QAForm': QA_form,
                    'replyForm': reply_form,
                    'qas': qas})
def home(request):
    reply_form = ReplyForms()
    # get image ranking dictionary
    question_ranking = r.zrange('questions_ranking', 0, -1, desc=True)[:10]
    question_ranking_ids = [int(id) for id in question_ranking]
    # get most viewed images
    most_replied = list(QA.objects.filter(
                           id__in=question_ranking_ids))
    most_replied.sort(key=lambda x: question_ranking_ids.index(x.id))

    paginator = Paginator(most_replied, 10)
    page = request.GET.get('page')
    try:
        most_replied  = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        most_replied = paginator.page(1)
    except EmptyPage:

        if request.is_ajax():

            # If the request is AJAX and the page is out of range
            # return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        most_replied = paginator.page(paginator.num_pages)
    if request.is_ajax():
            return render(request, 'qeustionsandswers/list_ajax.html', {'form': form, 'qas':qas})
    if request.user.is_authenticated:
        actions = Action.objects.exclude(user=request.user)
        following_ids = request.user.following.values_list('id',
                                                       flat=True)
        if following_ids:
        # If user is following others, retrieve only their actions
            actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related('user', 'user__profile')\
                     .prefetch_related('target')[:10]
        if request.method == 'POST':
            reply_form = ReplyForms(request.POST, initial={"form_type": "10"})
            if reply_form.is_valid():
                r_id = reply_form.cleaned_data['r_id']
                question = get_object_or_404(QA, id=r_id)
                new_question = reply_form.save(commit=False)
                new_question.user = request.user
                new_question.qa = question
                new_question.save()
                question.published = True
                question.save()
                create_action(request.user, 'replied on', question)
                r.zincrby('questions_ranking', 1, question.id)
                reply_form = ReplyForms()
        
        return render(request, 'qeustionsandswers/home.html', {'actions':actions, 'replyForm':reply_form, 'most_replied':actions})
    

  
    return render(request, 'qeustionsandswers/home.html', {'most_replied':most_replied})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})