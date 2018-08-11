from sendgrid.helpers.mail import *
import re
import sendgrid_shared as shared

def field_prompt(prompt_string):
    return prompt_string + ': '

def yes_no(prompt_string):
    return prompt_string + ' [Y|N] '

def validate_yesno(user_input):
    return re.match('^[Y|N]$', user_input.upper()) != None

def handle_user_input(prompt_string, match_condition=lambda input: input != ''):
    user_input = ''
    while True:
        user_input = raw_input(prompt_string).strip()
        if match_condition(user_input):
            break
        else:
            print('Invalid Input: Input does not satisfy the format requirements.')
    return user_input

def main():
    print('Welcome to the Email Sender!')
    while True:
        user_input = handle_user_input(yes_no('Do you want to send an email?'), validate_yesno).upper()
        if user_input == 'Y':
            from_email = Email(handle_user_input(field_prompt('Sender'), shared.validate_email))
            to_email = Email(handle_user_input(field_prompt('Recipient'), shared.validate_email))
            subject = handle_user_input(field_prompt('Subject Line'))
            content = Content('text/plain', handle_user_input(field_prompt('Message')))
            mail = Mail(from_email, subject, to_email, content)
            while True:
                attachment_prompt = handle_user_input(yes_no('Do you want to add an attachment?'), validate_yesno).upper()
                if attachment_prompt == 'Y':
                    mail.add_attachment(shared.create_attachment(handle_user_input('Filepath of Attachment: ', shared.validate_file)))
                    print('Attachment was successfully attached to the email.')
                elif attachment_prompt == 'N':
                    break
            shared.send_mail(mail)
        elif user_input == 'N':
            print('Bye!')
            break

if __name__ == '__main__':
    main()
