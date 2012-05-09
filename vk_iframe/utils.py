# -*- coding: utf-8 -*-
from django.conf import settings

# function borrowed from django-social-auth.utils
def setting(name, default=None):
    """Return setting value for given name or default value."""
    return getattr(settings, name, default)

def get_app_id():
    """
    If there is a setting with the name of Vk application ID,
    then loads ID from that setting. Otherwise - from default setting
    from previous versions of django-vkontakte-iframe
    This is done to avoid conflicts in settings names with other django apps
    """    
    if settings.VK_IFRAME_APP_ID_SETTING:
        return setting(settings.VK_IFRAME_APP_ID_SETTING)
    else:
        return settings.VK_APP_ID

def get_app_secret():
    """
    If there is a setting with the name of Vk application secret key,
    then loads secret key from that setting. Otherwise - from default setting
    from previous versions of django-vkontakte-iframe
    This is done to avoid conflicts in settings names with other django apps
    """
    if settings.VK_IFRAME_APP_SECRET_SETTING:
        return setting(settings.VK_IFRAME_APP_SECRET_SETTING)
    else:
        return settings.VK_APP_SECRET