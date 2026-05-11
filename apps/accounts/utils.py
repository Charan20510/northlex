import re
import requests
from django.conf import settings

PHONE_PATTERN = re.compile(r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}')


def send_otp_sms(mobile: str, otp_code: str) -> bool:
    """Send OTP via Fast2SMS. Returns True on success."""
    api_key = getattr(settings, 'SMS_API_KEY', '')
    if not api_key:
        # Dev fallback: print to console
        print(f'[DEV OTP] Mobile: {mobile}  OTP: {otp_code}')
        return True

    url = 'https://www.fast2sms.com/dev/bulkV2'
    payload = {
        'authorization': api_key,
        'variables_values': otp_code,
        'route': 'otp',
        'numbers': mobile.lstrip('+').lstrip('91'),
    }
    try:
        resp = requests.post(url, data=payload, timeout=10)
        data = resp.json()
        return data.get('return', False)
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
