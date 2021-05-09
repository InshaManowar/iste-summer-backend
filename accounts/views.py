from django.shortcuts import render, redirect,get_object_or_404,reverse
from django.contrib.auth import login, logout, authenticate
from accounts.forms import RegistrationForm, AccountAuthenticationForm
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import Account
from .utils import get_user

from summerschool.settings import LOGIN_REDIRECT_URL

def registration_view(request):
    context = {}
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # email = form.cleaned_data.get('email')
            # raw_password = form.cleaned_data.get('password1')
            # accounts = authenticate(email=email, password=raw_password)
            # login(request, accounts)
            return redirect(reverse('accounts:login'))
        else:
            context['registration_form'] = form
            
        
    else:
        form = RegistrationForm()
    context['registration_form'] = form
    return render(request, 'accounts/register.html', context)

def registrationConfirm_view(request):
    return render(request, 'accounts/register_confirm.html')

def logout_view(request):
	logout(request)
	return render (request, 'accounts/logout.html')

def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect(reverse(LOGIN_REDIRECT_URL))
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect(reverse(LOGIN_REDIRECT_URL))
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'accounts/login.html', context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_logged_in_user(request):
    context = {}
    serializer=UserSerializer(get_user(request))
    context['user']=serializer.data
    return Response(context)


