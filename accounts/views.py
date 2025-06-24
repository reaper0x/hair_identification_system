from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .utils import verify_email_verification_token, send_verification_email
from django.contrib.messages import get_messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from .serializers import RegisterSerializer

User = get_user_model()

# API Registration View
class RegisterView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            send_verification_email(user, request)
            return Response({'message': 'User registered successfully. Check your email to verify your account.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

# API Email Verification View
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({'error': 'Missing token'}, status=status.HTTP_400_BAD_REQUEST)

        user_id = verify_email_verification_token(token)
        if not user_id:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user.is_active:
            return Response({'message': 'Account already verified'}, status=status.HTTP_200_OK)

        user.is_active = True
        user.save()
        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)

# HTML-based signup view
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

# HTML-based login view
def login_view(request):
    list(get_messages(request))
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:home')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'login.html')

# Logout
def logout_view(request):
    logout(request)
    return redirect('accounts:login')

# Home page for logged in users
@login_required
def home_view(request):
    return render(request, 'home.html')

def signup_page(request):
    return render(request, 'signup.html')