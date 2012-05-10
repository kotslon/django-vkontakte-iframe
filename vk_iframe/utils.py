# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


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
    try:
        app_id = settings.VK_IFRAME_APP_ID
    except AttributeError:
        app_id = getattr(settings, 'VK_APP_ID', None)
        warnings.warn('VK_APP_ID is deprecated, please rename to VK_IFRAME_APP_ID',
                      DeprecationWarning)
    return app_id


def get_app_secret():
    """
    If there is a setting with the name of Vk application secret key,
    then loads secret key from that setting. Otherwise - from default setting
    from previous versions of django-vkontakte-iframe
    This is done to avoid conflicts in settings names with other django apps
    """
    try:
        app_secret = settings.VK_IFRAME_APP_SECRET
    except AttributeError:
        app_secret = getattr(settings, 'VK_APP_SECRET', None)
        warnings.warn('VK_APP_SECRET is deprecated, please rename to VK_IFRAME_APP_SECRET',
                      DeprecationWarning)
    return app_secret


def get_or_create_user(vk_id, defaults=None):
    """
    Get or create auth.User
    Depends on VK_IFRAME_USERNAME_IS_VK_ID setting (True by default):
    if True or absent gets(creates) User with username=vk_id,
    otherwise username is not relevant (even though it is still vk_id
    for new users) - search is done by vk_id
    """
    if setting('VK_IFRAME_USERNAME_IS_VK_ID', True):
        user, created = User.objects.get_or_create(username=str(vk_id),
                                                   defaults=defaults)
    else:
        defaults['username'] = str(vk_id)
        if hasattr(settings, 'VK_IFRAME_GET_VK_USER_FUNC'):
            found = True
            try:
                # Search in vk_profile first
                user = User.objects.get(vk_profile__vk_id=vk_id)
            except ObjectDoesNotExist:
                # Try to find user in the database YOUR way
                m = __import__(settings.VK_IFRAME_GET_VK_USER_FUNC['module'],
                        fromlist=[settings.VK_IFRAME_GET_VK_USER_FUNC['module']])
                f = getattr(m, settings.VK_IFRAME_GET_VK_USER_FUNC['function'])
                user, found = f(vk_id)
            if found:
                #TODO: find a better way to force profile update
                created = True  # we want to configure vk_profile
            else:
                user, created = User.objects.get_or_create(vk_profile__vk_id=vk_id,
                                                           defaults=defaults)
        else:
            user, created = User.objects.get_or_create(vk_profile__vk_id=vk_id,
                                                       defaults=defaults)
    return (user, created)


def is_vk_authenticated(user, viewer_id):
    is_va = False
    if user.is_authenticated():
        if setting('VK_IFRAME_USERNAME_IS_VK_ID', True):
            if user.username == viewer_id:
                is_va = True
        else:
            # check if current user has vk_profile with vk_id==viewer_id
            #TODO: check if it causes error when user has no vk_profile
            if user.vk_profile:
                if user.vk_profile.vk_id == viewer_id:
                    is_va = True
    return is_va
