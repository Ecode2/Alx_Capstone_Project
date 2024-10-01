from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, models

class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    

    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'password', 'token']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['id', 'token']

    
    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user
    
class PublicUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ['id', 'username', 'email']
