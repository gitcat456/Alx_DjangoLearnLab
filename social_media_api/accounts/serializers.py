from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token  # Required import
from django.db import models

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration with token creation"""
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(read_only=True)  # Token field
    
    class Meta:
        model = get_user_model()  # Using get_user_model()
        fields = [
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name', 'bio', 'token'
        ]
    
    def validate(self, data):
        """Validate passwords match"""
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                "password": "Passwords do not match"
            })
        return data
    
    def create(self, validated_data):
        """Create user and generate token"""
        validated_data.pop('password2')
        
        # Create user using get_user_model()
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            bio=validated_data.get('bio', '')
        )
        
        # Create token for the user
        token = Token.objects.create(user=user)
        
        # Add token to the user object for response
        user.token = token.key
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)  # Token field
    
    def validate(self, data):
        """Validate user credentials"""
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                
                # Get or create token
                token, created = Token.objects.get_or_create(user=user)
                data['user'] = user
                data['token'] = token.key
                return data
            raise serializers.ValidationError("Invalid credentials.")
        raise serializers.ValidationError("Must provide username and password.")