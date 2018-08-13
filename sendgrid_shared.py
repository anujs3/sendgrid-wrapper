import sendgrid
from sendgrid.helpers.mail import *
import re
import os
import urllib
import base64
import mimetypes
import time
import datetime

DAY_IN_SECONDS = 86400

def validate_email(email):
    return re.match('^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$', email.upper()) != None

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

def create_attachment(file_path):
    attachment = Attachment()
    attachment.content = get_content(file_path)
    attachment.type = get_mime(file_path)
    attachment.filename = get_basename(file_path)
    attachment.disposition = 'attachment'
    attachment.content_id = '{} File'.format(get_extension(file_path).upper())
    return attachment

def generate_timestamp(date):
    return int(time.mktime(datetime.datetime.strptime(date, '%m-%d-%Y %H:%M:%S').timetuple()))

def send_mail(mail):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    response = sg.client.mail.send.post(request_body=mail.get())
    print('\n{}\n{}\n{}'.format(response.status_code, response.body, response.headers))