from rest_framework import serializers
from .models import MyUser
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    class Meta:
        model = MyUser
        fields = ['email', 'full_name', 'gender', 'birthday', 'phone_number', 'job_code', 'job_title',
                  'officer_title', 'location_address', 'organization_name_path', 'organization_code_path',
                  'level', 'date_in', 'password', 'password2','token']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate(self, validated_data):
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')

        

        if password != password2:
            raise serializers.ValidationError({'password': 'password must match'})
        return validated_data
    
    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, 
                                     write_only=True,
                                     style={'input_type': 'password'})

    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'token': user.token,
        }