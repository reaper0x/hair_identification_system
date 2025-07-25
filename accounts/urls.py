from django.urls import path
from django.contrib import admin
from . import views
from .views import signup_page, index
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'accounts'

urlpatterns = [
    # HTML form-based views
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('signup/', signup_page, name='signup_page'),

    # API-based signup and email verification
    path('api/signup/', views.RegisterView.as_view(), name='api_signup'),
    path('verify-email/', views.VerifyEmailView.as_view(), name='verify_email'),

    # JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] 
