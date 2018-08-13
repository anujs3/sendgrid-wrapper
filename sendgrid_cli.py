from sendgrid.helpers.mail import *
import click
import sendgrid_shared as shared
import os
import time
import datetime

default_email = os.environ.get('DEFAULT_EMAIL')

@click.command()
@click.option('--sender', default=default_email, help='The Email Address for Sending Mail')
@click.option('--recipient', default=default_email, help='The Email Address for Receiving Mail')
@click.option('--subject', default='Test', help='The Subject Line')
@click.option('--message', default='This is a test.', help='Body of the Email')
@click.option('--attachmentlist', help='Text File with File Paths of Attachments')
@click.option('--schedule', help='Date/Time to Send Email')
@click.option('--cc', help='Email Address for Carbon Copy')
@click.option('--bcc', help='Email Address for Blocked Carbon Copy')
def main(sender,recipient,subject,message, attachmentlist, schedule, cc, bcc):
    if shared.validate_email(sender) and shared.validate_email(recipient):
        from_email = Email(sender)
        to_email = Email(recipient)
        content = Content('text/plain', message)
        mail = Mail(from_email, subject, to_email, content)
        if attachmentlist != None:
            with open(attachmentlist) as file:
                for line in file.readlines():
                    line = line.strip()
                    mail.add_attachment(shared.create_attachment(line))
        if schedule != None:
            timestamp = int(time.mktime(datetime.datetime.strptime(schedule, '%m-%d-%Y %H:%M:%S').timetuple()))
            if shared.validate_scheduled_date(timestamp):
                mail.send_at = timestamp
            else:
                error_handler('Error: The scheduled date is not valid.')
        if cc != None and shared.validate_email(cc):
            mail.personalizations[0].add_cc(Email(cc))
        if bcc != None and shared.validate_email(bcc):
            mail.personalizations[0].add_bcc(Email(bcc))
        shared.send_mail(mail)
    else:
        error_handler('Error: One or more emails are invalid.')

def error_handler(error_message, exit_code=1):
    click.echo(error_message)
    exit(exit_code)

if __name__ == '__main__':
    main()