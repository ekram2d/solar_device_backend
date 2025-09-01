import re
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.permissions import BasePermission
from .login_serializers import LoginSerializer  # Better than HttpResponse for structured data
from .serializers import RegisterSerializer, SolarDeviceSerializer, CustomUserSerializer,BankInformationSerializer,BrandDevicesSerializer,DeviceInformationSerializer,DeviceLocationSerializer,InverterSerializer
from .models import CustomUser, Devices,BankInformation,BrandInformation,DeviceInformation,DeviceLocation,Inverter

class RegisterViewSet(viewsets.ViewSet):
    # permission_classes = (AllowAny) 

    def create(self, request):
        # print("RegisterViewSet create method called with data:", request.data)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # print("Serializer is valid:", serializer.validated_data)
            # print("request",request.data)
            email = request.data.get('email')
            phone = request.data.get('phone_number')

            if CustomUser.objects.filter(phone_number=phone).exists():
                return JsonResponse({'message': 'Phone number already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            if CustomUser.objects.filter(user__email=email).exists():
                return JsonResponse({'message': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            print("RegisterViewSet create method called")
            serializer.save()
            return JsonResponse({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class AuthViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            custom_user = serializer.validated_data['custom_user']
            # print("Login successful for user:", custom_user.id)
            return Response({
                'message': 'Login successful',
                'user_id': user.id,
                'email': user.email,
                'username': user.username,
                'custom_user_id': custom_user.id,
                'refresh': serializer.validated_data['refresh'],
                'access': serializer.validated_data['access'],
                'user_type':custom_user.user_type,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'phone_number':custom_user.phone_number
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Custom permission
class IsCustomAdmin(BasePermission):
    """
    Allow access only to users with user_type='admin'
    """

    def has_permission(self, request, view):
        # print(request.user.user_type)
        if not request.user or not request.user.is_authenticated:
            return False
        
        # check related CustomUser model
        if hasattr(request.user, "custom_user_app2"):
            return request.user.custom_user_app2.user_type == "admin"
        return False

# ✅ ViewSet restricted to custom admins
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomAdmin]




# class SolarDeviceViewSet(viewsets.ViewSet):

#     def list(self, request):
#         user_id = request.query_params.get('user_id')
#         if not user_id:
#             return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

#         devices = Devices.objects.filter(user_id=user_id)
#         serializer = SolarDeviceSerializer(devices, many=True)
#         if not serializer.data:
#             return Response({"devices": 'No devices found'}, status=status.HTTP_200_OK)
#         return Response({"devices": serializer.data}, status=status.HTTP_200_OK)

class SolarDeviceViewSet(viewsets.ModelViewSet):
    serializer_class = SolarDeviceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Devices.objects.filter(user_id=user_id)
        return Devices.objects.none()
class BankInformationViewSet(viewsets.ModelViewSet):
    serializer_class = BankInformationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        custom_user = getattr(user, 'custom_user_app2', None)
        print(user.custom_user_app2.user_type)
        if user.custom_user_app2.user_type=='admin':
            return BankInformation.objects.all()
        else:
            return BankInformation.objects.filter(custom_user=custom_user)
        return BankInformation.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        # print(user)
        custom_user = getattr(user, 'custom_user_app2', None)
        if not custom_user:
            raise Exception("Custom user not found for the current user.")

        # print("Raw request data:", self.request.data)
        # print("Validated data:", serializer.validated_data)

        serializer.save(custom_user=custom_user)




class BrandInformationViewSet(viewsets.ModelViewSet):
    queryset = BrandInformation.objects.all()
    serializer_class = BrandDevicesSerializer

    def create(self, request, *args, **kwargs):
        brand_name = request.data.get('brand_name')
        brand_image = request.data.get('brand_image')

        if not brand_name or not brand_image:
            return Response(
                {"error": "❌ brand_name and brand_image cannot be null or empty."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if BrandInformation.objects.filter(brand_name__iexact=brand_name).exists():
            return Response(
                {"error": "❌ You already added a brand with this name."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            brand = BrandInformation.objects.get(pk=pk)
        except BrandInformation.DoesNotExist:
            return Response({"error": "Brand not found"}, status=status.HTTP_404_NOT_FOUND)

        brand_name = request.data.get('brand_name')
        if BrandInformation.objects.filter(brand_name__iexact=brand_name).exclude(pk=pk).exists():
            return Response({"error": "❌ You already added a brand with this name."}, status=400)

        serializer = self.get_serializer(brand, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            brand = BrandInformation.objects.get(pk=pk)
            brand.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BrandInformation.DoesNotExist:
            return Response({"error": "Brand not found"}, status=status.HTTP_404_NOT_FOUND)






class DeviceInformationViewSet(viewsets.ModelViewSet):
    queryset = DeviceInformation.objects.all()
    serializer_class = DeviceInformationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    

    def get_queryset(self):
        queryset = super().get_queryset()
        custom_user = self.kwargs.get("custom_user")
        if custom_user:
            queryset = queryset.filter(custom_user=custom_user,Check='pending')
        return queryset

    def partial_update(self, request, *args, **kwargs):
        """
        PATCH /device-info/<id>/ endpoint
        - If request contains 'Check', update Check status.
        - If request contains 'signature', upload signature only if null.
        """
        instance = self.get_object()

        # ✅ Case 1: Confirm check status
        check_status = request.data.get("Check")
        if check_status:
            instance.Check = check_status
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # ✅ Case 2: Upload signature
        signature_file = request.FILES.get("signature")
        if signature_file:
            if instance.signature:
                return Response(
                    {"error": "❌ Signature already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            instance.signature = signature_file
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {"error": "❌ No valid data provided."},
            status=status.HTTP_400_BAD_REQUEST
        )

class InverterViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Inverter.objects.all()
    serializer_class = InverterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class DeviceLocationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DeviceLocation.objects.all()
    serializer_class = DeviceLocationSerializer
    
    
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            print(refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()  # ⛔ will fail if refresh token is invalid
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"error": "Refresh token missing"}, status=status.HTTP_400_BAD_REQUEST)
