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
def main(sender,recipient,subject,message, attachmentlist, schedule):
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
                click.echo('Error: The scheduled date is not valid.')
                return
        shared.send_mail(mail)
    else:
        click.echo('Error: One or more emails are invalid.')

if __name__ == '__main__':
    main()