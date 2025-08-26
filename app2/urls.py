from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogoutView, RegisterViewSet, AuthViewSet, SolarDeviceViewSet, CustomUserViewSet,BankInformationViewSet,BrandInformationViewSet,DeviceInformationViewSet,DeviceLocationViewSet,InverterViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'devices', SolarDeviceViewSet, basename='devices')
router.register(r'customuser', CustomUserViewSet, basename='customuser')
router.register(r'bank-info', BankInformationViewSet, basename='bank-info')
router.register(r'brand-info', BrandInformationViewSet, basename='brand-info')
router.register(r'device-info', DeviceInformationViewSet, basename='device-info')
router.register(r'inverter', InverterViewSet, basename='inverter')
router.register(r'device-location',DeviceLocationViewSet,basename='device-location')
urlpatterns = [
    path("", include(router.urls)),  
    path("device-info/brand/<int:custom_user>/", DeviceInformationViewSet.as_view({"get": "list"})),
    path("device-info/sign/<int:pk>/", DeviceInformationViewSet.as_view({"patch": "partial_update"})),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="auth_logout"),
]