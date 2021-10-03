# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

def send_twilio_message(target_number, username, fact):
    account_sid = 'ACd2dda6bfec745c73e72e52824b5f5a19'
    auth_token = '195a146b33e315f9785dca6205274f53'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            messaging_service_sid='MG0680f2e81cfebfa5acff62631e268d1c',
            body='Greetings {}, Heres your fact for the day : {}'.format(username, fact),
            to=target_number
        )
    return True    
