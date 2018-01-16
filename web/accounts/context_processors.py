from django.contrib.auth.password_validation import password_validators_help_text_html
from django.utils.html import mark_safe

def password_validators(request):
    return {
        'password_validators_help_text_html': mark_safe(password_validators_help_text_html)
    }
