

import smtplib
from email.message import EmailMessage
import os
import sendgrid
import sendgrid.helpers.mail as sgm
import base64


###############################################################################################################################################

def PrepAttachment(attach_file_address):
    with open(attach_file_address, 'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    attachment = sgm.Attachment()
    attachment.file_content = sgm.FileContent(encoded)
    if attach_file_address[-4:].lower() in ['jpeg', '.png', '.jpg', '.gif']:
        attachment.file_type = sgm.FileType("image/jpeg")
    else:
        attachment.file_type = sgm.FileType("application/pdf")
    attachment.file_name = sgm.FileName(os.path.basename(attach_file_address))
    attachment.disposition = sgm.Disposition("attachment")
    return attachment



def SendEmail(to_email_addresses, subject, body, body_html=None, attach_file_address=None, cc_email_addresses=None, bcc_email_addresses=None):

    from_email = "Admin@puritanlife.com"
    mail = sgm.Mail(from_email=from_email, to_emails=to_email_addresses, subject=subject, plain_text_content=body, html_content=body_html)
    mail.reply_to = sgm.ReplyTo('eric.dire@puritanlife.com')

    if attach_file_address != None:
        if type(attach_file_address) != list:
            attach_file_address = [attach_file_address]
        for file_address in attach_file_address:
            attachment = PrepAttachment(file_address)
            mail.add_attachment(attachment)

    if cc_email_addresses != None:
        for email_address in cc_email_addresses:
            mail.add_cc(email_address)

    if bcc_email_addresses != None:
        for email_address in bcc_email_addresses:
            mail.add_bcc(email_address)

    sg = sendgrid.SendGridAPIClient(api_key = os.environ.get('SendGridAPIKey'))
    sg.send(mail)



###############################################################################################################################################


#import imghdr #for attaching pictures to email
#body_html = textile.textile(string)

def SendEmailCred(to_email_addresses, subject, body, body_html=None, attach_file_address=None, cc_email_addresses=None):

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



###############################################################################################################################################


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
