import random

from django import template
from django.conf import settings
from django.contrib.auth.models import User

from radio.models import Profile, SiteOption

register = template.Library()

# anonymous time seting
@register.simple_tag()
def settings_anonymous_time():
    return getattr(settings, 'ANONYMOUS_TIME', 0)

# Get user time setting
@register.simple_tag()
def get_user_time(user):
    print("Template TAG USER {}".format(user))
    history = {}
    if user.is_authenticated:
        print("I am logged in")
        user_profile = Profile.objects.get(user=user)
    else:
        print("I am AnonymousUser")
        try:
            anon_user = User.objects.get(username='ANONYMOUS_USER')
        except User.DoesNotExist:
            raise ImproperlyConfigured('ANONYMOUS_USER is missing from User table, was "./manage.py migrations" not run?')
        user_profile = Profile.objects.get(user=anon_user)
    if user_profile:
        history.update(minutes = 0)
    else:
        history.update(minutes = settings.ANONYMOUS_TIME)
    history.update(hours = history['minutes'] / 60)
    if history['minutes'] % 60 == 0:
        if history['minutes'] % 1440 == 0:
            history.update(display = '{} days'.format(history['minutes'] // 1440))
        else:
            history.update(display = '{} hours'.format(history['minutes'] // 60))
    else:
        history.update(display = '{} minutes'.format(history['minutes']))
    return history


# Allow settings in VISABLE_SETTINGS to be aviliable
@register.simple_tag()
def get_setting(value):
    visable_settings = getattr(settings, 'VISABLE_SETTINGS', None)
    if value in visable_settings:
        return getattr(settings, value, False)
    for opt in SiteOption.objects.filter(name=value, javascript_visible=True):
        return opt.value_boolean_or_string()
    return None
    
