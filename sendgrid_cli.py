from sendgrid.helpers.mail import Email, Content, Mail, Category
import click
import sendgrid_shared as shared
import os

default_email = os.environ.get('DEFAULT_EMAIL')


@click.command()
@click.option('--sender', default=default_email, help='The Email Address for Sending Mail')
@click.option('--recipient', default=default_email, help='The Email Address for Receiving Mail')
@click.option('--subject', default='Test', help='The Subject Line')
@click.option('--message', default='This is a test.', help='Body of the Email')
@click.option('--receivers', help='Email Addresses of Other Recipients')
@click.option('--attachments', help='Text File with File Paths of Attachments')
@click.option('--categories', help='Comma Separated List of Categories')
@click.option('--schedule', help='Date/Time to Send Email')
@click.option('--cc', help='Email Address(es) for Carbon Copies')
@click.option('--bcc', help='Email Address(es) for Blocked Carbon Copies')
def main(sender, recipient, subject, message, receivers, attachments, categories, schedule, cc, bcc):
    if shared.validate_email(str(sender)) and shared.validate_email(str(recipient)):
        from_email = Email(sender)
        to_email = Email(recipient)
        message_content = Content('text/plain', shared.message_handler(message))
        new_mail = Mail(from_email, subject, to_email, message_content)
        receiver_handler(receivers, new_mail)
        cc_handler(cc, new_mail)
        bcc_handler(bcc, new_mail)
        attachment_handler(attachments, new_mail)
        category_handler(categories, new_mail)
        schedule_handler(schedule, new_mail)
        shared.send_mail(new_mail)
    else:
        error_handler('One or more emails are invalid.')


def receiver_handler(receivers, new_mail):
    if receivers is not None:
        list_of_emails = receivers.split(';')
        for email_address in list_of_emails:
            if shared.validate_email(email_address):
                new_mail.personalizations[0].add_to(Email(email_address))
            else:
                error_handler('The recipient email address ({}) is invalid.'.format(email_address))


def cc_handler(cc, new_mail):
    if cc is not None:
        list_of_emails = cc.split(';')
        for email_address in list_of_emails:
            if shared.validate_email(email_address):
                new_mail.personalizations[0].add_cc(Email(email_address))
            else:
                error_handler('The CC email address ({}) is invalid.'.format(email_address))


def bcc_handler(bcc, new_mail):
    if bcc is not None:
        list_of_emails = bcc.split(';')
        for email_address in list_of_emails:
            if shared.validate_email(email_address):
                new_mail.personalizations[0].add_bcc(Email(email_address))
            else:
                error_handler('The BCC email address ({}) is invalid.'.format(email_address))


def attachment_handler(attachments, new_mail):
    if attachments is not None and shared.validate_file(attachments):
        with open(attachments) as file:
            for line in file.readlines():
                line = line.strip()
                if shared.validate_file(line):
                    new_mail.add_attachment(shared.create_attachment(line))


def category_handler(categories, new_mail):
    if categories is not None:
        list_of_categories = categories.split(',')
        for category in list_of_categories[:shared.MAX_NUMBER_OF_CATEGORIES]:
            new_mail.categories.append(Category(category))


def schedule_handler(schedule, new_mail):
    if schedule is not None:
        timestamp = shared.generate_timestamp(schedule)
        if shared.validate_date(timestamp):
            new_mail.send_at = timestamp
        else:
            error_handler('The scheduled date is not valid.')


def error_handler(error_message, exit_code=1):
    click.echo('Error: ' + error_message)
    exit(exit_code)


if __name__ == '__main__':
    main()
