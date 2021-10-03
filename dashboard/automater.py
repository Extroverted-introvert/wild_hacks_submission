from datetime import datetime, time
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from dashboard.models import SubscribedUser
from dashboard.read_facts import random_facts
from dashboard.twilio_module import send_twilio_message


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_messages, 'interval', minutes=5)
    scheduler.start()

def send_messages():
    time_range = [datetime.now(), datetime.now() + timedelta(minutes = 5)]
    target_data =SubscribedUser.objects.filter(next_message_time__range = time_range, is_subscribed = True)
    random_fact_list = random_facts(len(target_data))
    for ele in tuple(zip(target_data, random_fact_list)):
        flag = send_twilio_message(ele[0].number, ele[0].user.username, ele[1])

    for object in target_data:
        object.next_message_time = object.next_message_time + object.prefered_frequency
        object.save()

def get_days(prefered_freq):
    if prefered_freq == 'daily':
        return timedelta(days =1)
    elif prefered_freq == 'weekly':
        return timedelta(days =7)
    elif prefered_freq == 'monthy':
        return timedelta(month =1)