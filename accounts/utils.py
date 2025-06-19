import jwt
from django.conf import settings
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.urls import reverse

def generate_email_verification_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=24),  # valid for 24 hours
        'type': 'email_verification'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

def verify_email_verification_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        if payload.get('type') != 'email_verification':
            return None
        return payload.get('user_id')
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def send_verification_email(user, request):
    token = generate_email_verification_token(user)
    verification_url = request.build_absolute_uri(
        reverse('accounts:verify_email') + f'?token={token}'
    )
    subject = 'Verify your email'
    message = f'Hi {user.username}, please verify your email by clicking this link: {verification_url}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
