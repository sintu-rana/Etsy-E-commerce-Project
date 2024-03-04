from rest_framework import serializers
from Etsy.models.customer import Customer

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    
class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'email', 'password']

    def validate(self, data):
        return data
    

