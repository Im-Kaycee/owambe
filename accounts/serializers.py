from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role', 'bio', 'profile_picture', 'whatsapp_number', 'twitter', 'instagram', 'facebook')
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            role=validated_data.get('role', 'user'),
            bio=validated_data.get('bio', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user  