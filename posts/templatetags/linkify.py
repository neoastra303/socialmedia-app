import re
from django import template
from django.urls import reverse

register = template.Library()

@register.filter
def linkify_mentions(value):
    if not value:
        return value
    value = re.sub(
        r'@(\w+)',
        r'<a href="' + reverse('users:profile', args=['__USERNAME__']).replace('__USERNAME__', r'\1') + r'">@\1</a>',
        str(value)
    )
    return value

@register.filter
def linkify_hashtags(value):
    if not value:
        return value
    value = re.sub(
        r'#(\w+)',
        r'<a href="' + reverse('posts:hashtag_posts', args=['__HASHTAG__']).replace('__HASHTAG__', r'\1') + r'">#\1</a>',
        str(value)
    )
    return value

@register.filter
def linkify(value):
    value = linkify_mentions(value)
    value = linkify_hashtags(value)
    return value
