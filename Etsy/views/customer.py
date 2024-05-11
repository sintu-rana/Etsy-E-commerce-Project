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
from Etsy.models.customer import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import admin
from django.urls import path
from Etsy.serializers.customer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    authentication_classes,
    permission_classes,
    api_view,
)
from rest_framework import generics, permissions, viewsets


@api_view()
def view_dtl(request):
    return Response({"msg":"Welcome in our World !."})



class CustomUserList(generics.ListCreateAPIView):
    serializer_class = CustomUserMainSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = CustomUser.objects.exclude(username='admin')

        # client_id = self.request.query_params.get('client_id')
        # site_id = self.request.query_params.get('site_id')

        # if client_id:
        #     queryset = queryset.filter(client_id=client_id)

        # if site_id:
        #     queryset = queryset.filter(site_id=site_id)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)

        if queryset.exists():
            return Response({"status": True, "message": "Data retrieved successfully", "data": serializer.data})
        else:
            return Response({"status": False, "message": "No data available", "data": []})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        user_id = user.id

        response_data = {
            "status": True,
            "message": "User created successfully",
            "user_id": user_id
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    
    
    
class CustomUserCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserMainSerializer
    permission_classes = [permissions.AllowAny]

# from django.contrib.auth.hashers import check_password, make_password

# class CustomerLoginView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         customer = Customer.objects.filter(email=email).first()

#         if customer and check_password(password, customer.password):
#             refresh = RefreshToken.for_user(customer)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# class CustomerLoginView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         # Retrieve the customer object by email
#         customer = Customer.objects.filter(email=email).first()

#         # Check if customer exists and if the provided password is correct
#         if customer and check_password(password, customer.password):
#             # Generate refresh and access tokens
#             refresh = RefreshToken.for_user(customer)
            
#             # Return the tokens in the response
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }, status=status.HTTP_200_OK)
#         else:
#             # Return unauthorized if credentials are invalid
#             return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



# class SignupView(APIView):
#     def post(self, request):
#         serializer = SignupSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         customer = Customer.objects.create(
#             first_name=serializer.validated_data['first_name'],
#             last_name=serializer.validated_data['last_name'],
#             phone=serializer.validated_data['phone'],
#             email=serializer.validated_data['email'],
#             password=make_password(serializer.validated_data['password'])
#         )

#         return Response({'detail': 'Signup successful'}, status=status.HTTP_201_CREATED)


# @api_view(['GET'])
# def logout(request):
#     request.session.clear()
#     return redirect(reverse('login'))



from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
    ROLES = {
        "Site Incharge": "1",
        "Site Engineer": "2",
        "Security": "3",
        "Labour": "4",
        "Store": "5",
        "HSE": "6",
        "Admin": "7"
    }

    def get_token(self, user):
        token = super().get_token(user)

        # Get related Client and Site IDs
        client_ids = user.client_id.values_list('id', flat=True)
        site_ids = user.site_id.values_list('id', flat=True)

        # Include client_ids and site_ids in the token payload
        token['client_ids'] = ','.join(map(str, client_ids))
        token['site_ids'] = ','.join(map(str, site_ids))

        return token


    def post(self, request, *args, **kwargs):
        # Get the username, password, and custom_user_role from the request
        username = request.data.get('username')
        password = request.data.get('password')
        custom_user_role = request.data.get('custom_user_role')

        # Check if both username and password are provided
        if not username or not password:
            response_data = {"status": False, "message": "Both username and password are required."}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # Find the user based on the provided username
        user = CustomUser.objects.filter(username=username).first()

        errors = {}

        # Check if the user exists based on the provided username
        if user is None:
            errors["username"] = ["User not found."]
        elif user.is_superuser:
            # Superusers don't need custom_user_role
            pass
        else:
            # Check for password validity
            if not user.check_password(password):
                errors["password"] = ["Invalid password."]

            # Check if custom_user_role is provided
            if custom_user_role is None:
                errors["custom_user_role"] = ["custom_user_role is required."]
            else:
                # Check if the user's custom_user_role matches the provided custom_user_role
                if user.custom_user_role != int(custom_user_role):  # Cast to integer
                    errors["custom_user_role"] = ["Invalid custom_user_role for login"]

        if errors:
            response_data = {"status": False, "message": "Authentication failed", "errors": errors}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # If everything is valid, proceed with token generation
        response = super().post(request, *args, **kwargs)
        # user_type_choices = dict(CustomUser.USER_TYPE)
        user_data = {
            "username": user.username,
            "custom_user_role": user.custom_user_role,
            "id": user.id,
            "access": response.data["access"],
            "refresh": response.data["refresh"],
            "roles": self.ROLES,
        }
        response_data = {
            "status": True,
            "message": "Authentication successful",
            "data": user_data
        }
        return Response(response_data)
  
  
from django.contrib.auth import authenticate, login, logout  
    
class LogoutView(APIView):
    def post(self, request):
        # Optionally, you can perform additional logout logic here
        user = request.user
        if user.is_authenticated:
            user.fcm_token = None  # Assuming you have a field named fcm_token in your CustomUser model
            user.save()
            logout(request)
            return Response({'status': True,'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False, 'message': 'User is not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
