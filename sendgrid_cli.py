from sendgrid.helpers.mail import *
import click
import sendgrid_shared as shared
import os

default_email = os.environ.get('DEFAULT_EMAIL')

@click.command()
@click.option('--sender', default=default_email, help='The Email Address for Sending Mail')
@click.option('--recipient', default=default_email, help='The Email Address for Receiving Mail')
@click.option('--subject', default='Test', help='The Subject Line')
@click.option('--message', default='This is a test.', help='Body of the Email')
@click.option('--attachments', help='Text File with File Paths of Attachments')
@click.option('--schedule', help='Date/Time to Send Email')
@click.option('--cc', help='Email Address for Carbon Copy')
@click.option('--bcc', help='Email Address for Blocked Carbon Copy')
def main(sender,recipient,subject,message, attachments, schedule, cc, bcc):
    if shared.validate_email(sender) and shared.validate_email(recipient):
        from_email = Email(sender)
        to_email = Email(recipient)
        content = Content('text/plain', message)
        mail = Mail(from_email, subject, to_email, content)
        attachment_handler(attachments, mail)
        schedule_handler(schedule, mail)
        cc_handler(cc, mail)
        bcc_handler(bcc, mail)
        shared.send_mail(mail)
    else:
        error_handler('One or more emails are invalid.')

def attachment_handler(attachments, mail):
    if attachments != None:
        with open(attachments) as file:
            for line in file.readlines():
                line = line.strip()
                mail.add_attachment(shared.create_attachment(line))

def schedule_handler(schedule, mail):
    if schedule != None:
        timestamp = shared.generate_timestamp(schedule)
        if shared.validate_date(timestamp):
            mail.send_at = timestamp
        else:
            error_handler('The scheduled date is not valid.')

def cc_handler(cc, mail):
    if cc != None:
        if shared.validate_email(cc):
            mail.personalizations[0].add_cc(Email(cc))
        else:
            error_handler('The CC email is invalid.')

def bcc_handler(bcc, mail):
    if bcc != None:
        if shared.validate_email(bcc):
            mail.personalizations[0].add_bcc(Email(bcc))
        else:
            error_handler('The BCC email is invalid.')

def error_handler(error_message, exit_code=1):
    click.echo('Error: ' + error_message)
    exit(exit_code)

if __name__ == '__main__':
    main()