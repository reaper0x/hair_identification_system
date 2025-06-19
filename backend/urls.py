from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),       # JWT login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),       # JWT refresh
    path('', lambda request: redirect('accounts:login')),  # redirect root to /accounts/login/
]
