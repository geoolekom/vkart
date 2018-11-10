import vk
from django.conf import settings


def get_api():
    session = vk.Session(access_token=settings.VKAPI_ACCESS_TOKEN)
    return vk.API(session, v=settings.VKAPI_VERSION)


def get_api_by_token(access_token):
    session = vk.Session(access_token=access_token)
    return vk.API(session, v=settings.VKAPI_VERSION)
