import re
import requests
from django.core.mail import send_mail
from django.conf import settings

PHONE_PATTERN = re.compile(r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}')


def send_otp_sms(mobile: str, otp_code: str) -> bool:
    """Send OTP via Fast2SMS. Returns True on success."""
    api_key = getattr(settings, 'SMS_API_KEY', '')
    if not api_key:
        # Dev fallback: print to console
        print(f'[DEV OTP] Mobile: {mobile}  OTP: {otp_code}')
        return True

    digits = re.sub(r'\D', '', mobile)
    if digits.startswith('91') and len(digits) > 10:
        digits = digits[-10:]

    url = 'https://www.fast2sms.com/dev/bulkV2'
    payload = {
        'authorization': api_key,
        'variables_values': otp_code,
        'route': 'otp',
        'numbers': digits,
    }
    try:
        resp = requests.post(url, data=payload, timeout=10)
        data = resp.json()
        return data.get('return', False)
    except Exception:
        return False


def send_otp_email(email: str, otp_code: str, mobile: str | None = None) -> bool:
    """Send OTP to email. Returns True when the mail backend accepts it."""
    if not email:
        return False

    subject = 'Your NorthLex OTP'
    message_lines = [
        'Your NorthLex login OTP is:',
        '',
        otp_code,
        '',
        'This OTP is valid for 10 minutes.',
    ]
    if mobile:
        message_lines.extend(['', f'Mobile: {mobile}'])

    try:
        send_mail(
            subject=subject,
            message='\n'.join(message_lines),
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
            recipient_list=[email],
            fail_silently=False,
        )
        return True
    except Exception:
        return False


def sanitize_message(content: str) -> str:
    """Replace phone number patterns with [Contact via Admin]."""
    return PHONE_PATTERN.sub('[Contact via Admin]', content)


def normalize_mobile(mobile: str) -> str:
    """Strip spaces/dashes, ensure starts with +91."""
    digits = re.sub(r'\D', '', mobile)
    if len(digits) == 10:
        return f'+91{digits}'
    if len(digits) == 12 and digits.startswith('91'):
        return f'+{digits}'
    return f'+{digits}'
