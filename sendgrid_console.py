from sendgrid.helpers.mail import Email, Content, Mail
import re
import sendgrid_shared as shared


def field_prompt(prompt_string):
    assert type(prompt_string) == str
    return prompt_string + ': '


def boolean_formatter(prompt_string):
    assert type(prompt_string) == str
    return prompt_string + ' [Y|N] '


def validate_boolean(user_input):
    assert type(user_input) == str
    return re.match('^[Y|N]$', user_input.upper()) is not None


def boolean_question(prompt_string):
    assert type(prompt_string) == str
    return handle_user_input(boolean_formatter(prompt_string), validate_boolean).upper()


def email_creator(prompt_string):
    assert type(prompt_string) == str
    return Email(handle_user_input(field_prompt(prompt_string), shared.validate_email))


def attachment_uploader(new_mail):
    new_mail.add_attachment(shared.create_attachment(handle_user_input('File Path of Attachment: ', shared.validate_file)))
    print('Attachment was successfully attached to the email.')


def handle_user_input(prompt_string, match_condition=lambda input: input != ''):
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
        send_boolean = boolean_question('Do you want to send an email?')
        if send_boolean == 'Y':
            from_email = email_creator('Sender')
            to_email = email_creator('Recipient')
            subject = handle_user_input(field_prompt('Subject Line'))
            message_content = Content('text/plain', shared.message_handler(handle_user_input(field_prompt('Message'))))
            new_mail = Mail(from_email, subject, to_email, message_content)
            while True:
                to_boolean = boolean_question('Do you want to send it to anyone else?')
                if to_boolean == 'Y':
                    new_mail.personalizations[0].add_to(email_creator('Email'))
                elif to_boolean == 'N':
                    break
            while True:
                cc_boolean = boolean_question('Do you want to CC anyone?')
                if cc_boolean == 'Y':
                    new_mail.personalizations[0].add_cc(email_creator('Email'))
                elif cc_boolean == 'N':
                    break
            while True:
                bcc_boolean = boolean_question('Do you want to BCC anyone?')
                if bcc_boolean == 'Y':
                    new_mail.personalizations[0].add_bcc(email_creator('Email'))
                elif bcc_boolean == 'N':
                    break
            while True:
                attachment_boolean = boolean_question('Do you want to add an attachment?')
                if attachment_boolean == 'Y':
                    attachment_uploader(new_mail)
                elif attachment_boolean == 'N':
                    break
            schedule_boolean = boolean_question('Do you want to schedule the email?')
            if schedule_boolean == 'Y':
                while True:
                    schedule = handle_user_input(field_prompt('Date/Time [MM-DD-YYYY HH:MM:SS]'))
                    timestamp = shared.generate_timestamp(schedule)
                    if shared.validate_date(timestamp):
                        new_mail.send_at = timestamp
                        break
                    else:
                        print('The scheduled date is not valid.')
            shared.send_mail(new_mail)
        elif send_boolean == 'N':
            print('Bye!')
            break


if __name__ == '__main__':
    main()
