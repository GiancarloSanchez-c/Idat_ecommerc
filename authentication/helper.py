from django.core.mail import EmailMessage

def send_email(data):
    email = EmailMessage(subject=data['subject'], body=data['body'], to=[data['to']])
    email.send()