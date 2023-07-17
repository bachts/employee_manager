from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

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
                  'job_code', 'job_title', 'officer_title',
                  'location_address', 'organization_name_path', 'organization_code_path',
                  'level', 'password', 'token']
        
    def create(self, validated_data):
        return User.objects._create_user(**validated_data)
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError('An email address is required')
        
        if password is None:
            raise serializers.ValidationError('A password is required')
        
        user = authenticate(email_address=email, password=password)
        if user is None:
            raise serializers.ValidationError('No user with email address found')
        if not user.is_active():
            raise serializers.ValidationError('User has been deactivated')
        return {
            'token': user.token,
        }

class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['email_address']    
