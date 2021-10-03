from datetime import datetime
from datetime import timedelta
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from dashboard.apps import DashboardConfig
import logging
from dashboard.models import SubscribedUser



logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return render(request, 'dashboard/dashboard_bootstrap.html')

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'dashboard/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            if request.POST['subscribe'] == "yes":
                return redirect("dashboard:subscription" )
            else: 
                return redirect("dashboard:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'dashboard/user_registration_bootstrap.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'dashboard/user_login_bootstrap.html', context)
    else:
        return render(request, 'dashboard/user_login_bootstrap.html', context)


def logout_request(request):
    logout(request)
    return redirect('dashboard:index')


def subscription(request):
    context ={}
    if request.method == 'GET':
        return render(request, 'dashboard/subscription_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        mobile = request.POST['mobile']
        prefered_time = request.POST['prefered_time']
        target_hour, target_minute = int(prefered_time.split(':')[0]), int(prefered_time.split(':')[1])
        target_time = target_hour*60 + target_minute
        prefered_freq = request.POST['prefered_freq']
        current_time =  datetime.now().hour*60 +datetime.now().minute

        if current_time < target_time:
            next_message_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, target_hour, target_minute, 0, 0)
        else:
            next_message_time = get_next_message_time(target_hour,target_minute,prefered_freq)    
        subscriber_exist = False
        try:
            user = User.objects.get(username= username)
            SubscribedUser.objects.get(user=user)
            subscriber_exist = True
        except:
            logger.error("New Subscriber")
        if not subscriber_exist:
            user = SubscribedUser.objects.create(user=user, number=mobile, prefered_time=prefered_time, next_message_time=next_message_time,
                                            prefered_frequency=prefered_freq, is_subscribed = True)
            return redirect("dashboard:index")
        else:
            context['message'] = "Subscriber already exists."
            return render(request, 'dashboard/dashboard_bootstrap.html', context)

def get_next_message_time(target_hour,target_minute,prefered_freq):
    if prefered_freq == 'daily':
        return datetime(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, target_hour, target_minute, 0) + timedelta(days=1)
    elif prefered_freq == 'weekly':
        return datetime(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, target_hour, target_minute, 0) + timedelta(days=7)
    elif prefered_freq == 'monthy':
        return datetime(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, target_hour, target_minute, 0) + timedelta(months=1)

