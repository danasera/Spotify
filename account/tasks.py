from spotify.celery import app


@app.task
def send_activation_mail(email, activation_code):
    from django.core.mail import send_mail
    message = f'Hello! Your activation code: {activation_code}'
    send_mail('Activation code',
              message,
              'test@gmail.com',
              [email])


