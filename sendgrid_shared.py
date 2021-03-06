from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Attachment
import re
import os
import urllib
import base64
import mimetypes
import time
import datetime

DAY_IN_SECONDS = 86400
MAX_NUMBER_OF_CATEGORIES = 10


def validate_email(email):
    assert type(email) == str or type(email) == unicode, 'The email ({}) is not valid because the type is {}.'.format(email, type(email))
    return re.match('^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$', email.upper()) is not None


def validate_file(file_path):
    return os.path.exists(file_path)


def validate_date(timestamp):
    current_time = time.time()
    return (current_time+60) <= timestamp <= current_time+(DAY_IN_SECONDS*3)


def get_basename(file_path):
    return os.path.basename(file_path)


def get_extension(file_path):
    return os.path.splitext(get_basename(file_path))[1]


def get_mime(file_path):
    return mimetypes.guess_type(urllib.pathname2url(file_path))[0]


def get_content(file_path):
    with open(file_path) as file:
        data = file.read()
    return base64.b64encode(data)


def message_handler(message):
    if validate_file(message):
        with open(message) as file:
            return file.read()
    else:
        return message


def create_attachment(file_path):
    new_attachment = Attachment()
    new_attachment.content = get_content(file_path)
    new_attachment.type = get_mime(file_path)
    new_attachment.filename = get_basename(file_path)
    new_attachment.disposition = 'attachment'
    new_attachment.content_id = '{} File'.format(get_extension(file_path).upper())
    return new_attachment


def generate_timestamp(date):
    return int(time.mktime(datetime.datetime.strptime(date, '%m-%d-%Y %H:%M:%S').timetuple()))


def send_mail(new_mail):
    sg = SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    try:
        response = sg.client.mail.send.post(request_body=new_mail.get())
        print('\n{}\n{}\n{}'.format(response.status_code, response.body, response.headers))
    except Exception as e:
        print('There was an unexpected error when trying to send the email.')

