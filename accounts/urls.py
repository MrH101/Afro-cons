from django.urls import path
from asosiyapp.views import HomeIndex2View
from django.conf import settings
from django.conf.urls.static import static
from .views import LoginView, LogoutView,VendorVerificationView, VendorDashboardView, CustomerDashboardView,VendorRegisterView, CustomerRegisterView,VendorDetailView



urlpatterns = [
    path('user/login/', LoginView.as_view(), name='login'),
    path('user/logout/', LogoutView.as_view(), name='logout'),
    path('vendor/register/', VendorRegisterView.as_view(), name='vendor_register'),
    path('customer/register/', CustomerRegisterView.as_view(), name='customer_register'),
    path('vendor/verification/', VendorVerificationView.as_view(), name='vendor_verification'),
    path('vendor/dashboard/', VendorDashboardView.as_view(), name='vendor_dashboard'),
    path('customer/dashboard/', CustomerDashboardView.as_view(), name='customer_dashboard'),
    path('vendor/<str:username>/',VendorDetailView.as_view(),name='vendor_detail'),
]