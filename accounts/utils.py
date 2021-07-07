from django.contrib.auth import get_user_model
from summerschool import settings
from summerschool.settings import IS_MAKING_DOCS

def get_user(request) :
    if IS_MAKING_DOCS:
        return get_user_model().objects.get(email='test@gmail.com')

    return request.user
    