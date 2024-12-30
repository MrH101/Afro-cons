from django.urls import path


from asosiyapp.views import HomeIndex2View
from django.conf import settings
from django.conf.urls.static import static

from userapp.views import LoginView, LogoutView, RegisterView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]