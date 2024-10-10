from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, models

class UserSerializer(serializers.ModelSerializer):
    """
    UserSerializer is a ModelSerializer for the User model that includes a custom token field.
    Fields:
        - id: The unique identifier for the user (read-only).
        - username: The username of the user.
        - email: The email address of the user.
        - password: The password of the user (write-only).
        - token: The authentication token for the user (read-only).
    Methods:
        - get_token(obj): Retrieves or creates an authentication token for the user.
        - create(validated_data): Creates a new user with the provided validated data.
    """
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
    """
    Serializer for public user information.

    This serializer is used to convert the User model instance into JSON format
    for public consumption. It includes the following fields:
    - id: The unique identifier for the user.
    - username: The username of the user.
    - email: The email address of the user.

    Attributes:
        Meta (class): A class used to define the model and fields to be serialized.
    """

    class Meta:
        model = models.User
        fields = ['id', 'username', 'email']
