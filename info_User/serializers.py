from rest_framework import serializers
from .models import InfoUser

class InfoSerializer(serializers.ModelSerializer):

    default_error_messages = {
        'username':'El usuario no debe de contener caracteres alfanuméricos'
    }
    class Meta:
        model = InfoUser
        fields = ['username','email','telefono','programa']

    def validate(self, attrs):
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(self.default_error_messages)
        return attrs
    
    def create(self, validated_data):
        return InfoUser.objects.create_user(**validated_data)

class TokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)