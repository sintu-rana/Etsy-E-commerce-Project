from rest_framework import serializers
from Etsy.models.customer import Customer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    
class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'email', 'password']

    def validate(self, data):
        return data
    
from rest_framework_simplejwt.views import TokenObtainPairView
from Etsy.models.customer import *

class CustomUserMainSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        """
        Check that the username is not already taken.
        """
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        # client_ids = validated_data.pop("client_id", None)
        # site_ids = validated_data.pop("site_id", None)

        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)

        instance.save()

        # if client_ids:
        #     instance.client_id.set(client_ids)

        # if site_ids:
        #     instance.site_id.set(site_ids)

        return instance

    class Meta:
        model = CustomUser
        fields = ["id", "username", "password", "custom_user_role", "email", "contact"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        user = self.user  # Get the user object
        
        if not user.status:
            # If user status is False, return a custom error message
            raise serializers.ValidationError("User is not allowed to log in.")

        # Include user data in the response
        serializer = CustomUserMainSerializer(user).data
        for key, value in serializer.items():
            data[key] = value

        return data