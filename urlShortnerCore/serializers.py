from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('userId', 'name', 'email', 'phone')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        token['email'] = user.email

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add extra responses to the JWT response if needed
        data.update({'userId': self.user.userId})
        data.update({'name': self.user.name})

        return data
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password')

        if not check_password(password, user.password):
            raise serializers.ValidationError('Invalid email or password')

        refresh = RefreshToken.for_user(user)
        return {
            'userId': user.userId,
            'name': user.name,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }