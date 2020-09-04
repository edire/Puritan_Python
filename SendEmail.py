

import smtplib
from email.message import EmailMessage
import os
#import imghdr #for attaching pictures to email


#body_html = textile.textile(string)


def SendEmail(to_email_addresses, subject, body, body_html=None, attach_file_address=None, cc_email_addresses=None):

    email_user = os.environ.get('SendGridUID')
    email_password = os.environ.get('SendGridPWD')
    from_email_address = 'Admin@puritanlife.com'

    msg = EmailMessage()
    msg['To'] = to_email_addresses
    if cc_email_addresses != None:
        msg['Cc'] = cc_email_addresses
#    msg['Bcc'] = ''
    msg['From'] = from_email_address
    msg['Reply-To'] = 'eric.dire@puritanlife.com'
    msg['Subject'] = subject
    msg.set_content(body)

    if body_html!=None:
        msg.add_alternative(body_html, subtype='html')

    if attach_file_address!=None:
        with open(attach_file_address, 'rb') as f:
            file_data = f.read()
            file_name = attach_file_address[attach_file_address.rfind('\\') + 1:]
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

#    with smtplib.SMTP('smtp.sendgrid.com', port=587) as smtp:
    with smtplib.SMTP_SSL('smtp.sendgrid.com', port=465) as smtp:
        smtp.login(email_user, email_password)
        smtp.send_message(msg)



# def SendEmailLocal(to_email_addresses, subject, body):
#     email_user = 'SSIS@local.ed'
#     email_password = 'SSIS2019Password'
#     from_email_address = 'Admin@puritanlife.com'
#     msg = EmailMessage()
#     msg['To'] = to_email_addresses
#     msg['From'] = from_email_address
#     msg['Reply-To'] = 'Brianna.Reams@puritanlife.com'
#     msg['Subject'] = subject
#     msg.set_content(body)
#     with smtplib.SMTP('localhost', port=25) as smtp:
#         smtp.login(email_user, email_password)
#         smtp.send_message(msg)



# if __name__ == '__main__':
#     SendEmailLocal('eric.dire@puritanlife.com', 'subject', 'body')
#     print('Sent')