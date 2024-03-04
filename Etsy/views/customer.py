from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.shortcuts import redirect
from django.urls import reverse
from Etsy.models.customer import Customer
from Etsy.serializers.customer import LoginSerializer, SignupSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view()
def view_dtl(request):
    return Response({"msg":"Welcome in our World !."})

from django.contrib.auth.hashers import check_password, make_password

class CustomerLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        customer = Customer.objects.filter(email=email).first()

        if customer and check_password(password, customer.password):
            refresh = RefreshToken.for_user(customer)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CustomerLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Retrieve the customer object by email
        customer = Customer.objects.filter(email=email).first()

        # Check if customer exists and if the provided password is correct
        if customer and check_password(password, customer.password):
            # Generate refresh and access tokens
            refresh = RefreshToken.for_user(customer)
            
            # Return the tokens in the response
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            # Return unauthorized if credentials are invalid
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer = Customer.objects.create(
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            phone=serializer.validated_data['phone'],
            email=serializer.validated_data['email'],
            password=make_password(serializer.validated_data['password'])
        )

        return Response({'detail': 'Signup successful'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def logout(request):
    request.session.clear()
    return redirect(reverse('login'))






