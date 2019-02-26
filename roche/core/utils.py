from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def is_valid_number(number):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    number_with_country_code = "+1" + number

    try:
        response = client.lookups.phone_numbers(number_with_country_code).fetch()
        return True
    except TwilioRestException as e:
        if e.code == 20404:
            return False
        else:
            return e

def send_sms(to, message):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    from = settings.TWILIO_NUMBER

   if is_valid_number(to): 

        message = client.messages.create(
                from = from,
                body = message,
                to = to,
                )

    else:
        return is_valid_number(to)
