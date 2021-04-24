from django.contrib.auth import get_user_model

IS_MAKING_DOCs=True

def get_user(request) :
    if IS_MAKING_DOCs:
        return get_user_model().objects.get(email='test@gmail.com')

    return request.user
    