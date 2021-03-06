from rest_framework import serializers
from .models import Account


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('email', 'registration_number', 'first_name', 'last_name')
