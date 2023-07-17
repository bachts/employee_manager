from rest_framework import serializers
from .models import User

class RegistrationSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    token = serializers.CharField(max_length=255, read_only=True,)

    class Meta:
        model = User
        fields = ['full_name', 'email_address', 'employee', 'phone_number',
                  'password', 'token']