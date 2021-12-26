import json

from django import template
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from ping.models import Opponent

user_model = get_user_model()

register = template.Library()


@register.filter
def opponent_details(opponent):
    if not isinstance(opponent, Opponent):
        return ""
    return format_html('{} {}', opponent.last_name.upper(), opponent.first_name.capitalize())


@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))
