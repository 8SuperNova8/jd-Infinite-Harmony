from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class EmailTokenObtainSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password =  data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalido el Email o contraseña')
        
        user =  authenticate(username=user.username, password= password)#la validacion se hace sobre el objeto de user consultado con email
        if not user:
            raise serializers.ValidationError('Invalido el Email o contraseña')
        refresh=  RefreshToken.for_user(user)

        return {
            'refresh':str(refresh),
            'access': str(refresh.access_token)
        }