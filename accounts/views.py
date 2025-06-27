from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import get_messages # Used for consuming messages
from .forms import CustomUserCreationForm # Import your CustomUserCreationForm
from .utils import verify_email_verification_token, send_verification_email # Imports from your .utils module
from rest_framework.views import APIView # For REST API views
from rest_framework.response import Response # For REST API responses
from rest_framework import status # For HTTP status codes
from rest_framework.permissions import AllowAny # For setting API permissions
from rest_framework.parsers import JSONParser # For parsing JSON request data
from .serializers import RegisterSerializer # Import your RegisterSerializer

User = get_user_model() # Get the active user model

# API Registration View
class RegisterView(APIView):
    """
    API view for user registration.
    Handles user creation, sets is_active to False, and sends a verification email.
    """
    permission_classes = [AllowAny] # Allow unauthenticated users to register
    parser_classes = [JSONParser] # Expect JSON data in the request body

    def post(self, request):
        """
        Handles POST requests for user registration.
        Validates data, creates user, sends verification email.
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save() # Save the user (password will be hashed)
            user.is_active = False # Set user to inactive until email is verified
            user.save()
            send_verification_email(user, request) # Send the verification email
            return Response(
                {'message': 'User registered successfully. Check your email to verify your account.'},
                status=status.HTTP_201_CREATED # 201 Created status
            )
        # If serializer is not valid, return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Changed to 400 Bad Request for validation errors

# API Email Verification View
class VerifyEmailView(APIView):
    """
    API view for email verification.
    Activates user account upon successful token verification.
    """
    permission_classes = [AllowAny] # Allow unauthenticated users to verify email

    def get(self, request):
        """
        Handles GET requests for email verification.
        Validates token from query parameters and activates user.
        """
        token = request.query_params.get('token') # Get token from URL query parameters
        if not token:
            return Response({'error': 'Missing token'}, status=status.HTTP_400_BAD_REQUEST)

        user_id = verify_email_verification_token(token) # Verify the token
        if not user_id:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id) # Retrieve the user
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user.is_active:
            return Response({'message': 'Account already verified'}, status=status.HTTP_200_OK)

        user.is_active = True # Activate the user account
        user.save()
        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)

# HTML-based signup view
def signup_view(request):
    """
    Handles user registration via an HTML form.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = True  # Attiva subito l'utente (opzionale)
            user.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('accounts:login')
        else:
            # Add form errors to Django messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').capitalize()}: {error}")
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    # Render the signup template
    return render(request, 'signup.html', {'form': form})

# HTML-based login view
def login_view(request):
    """
    Handles user login via an HTML form.
    Authenticates user with email and password.
    """
    from .forms import EmailAuthenticationForm
    list(get_messages(request))
    form = EmailAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('accounts:index')  # Redirect to index after login
            else:
                messages.error(request, 'Account not active. Please verify your email.')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'login.html', {'form': form})

# Logout view
def logout_view(request):
    """
    Logs out the current user and redirects to the login page.
    """
    logout(request)
    messages.info(request, "You have been logged out successfully.") # Logout message
    return redirect('accounts:login') # Redirect to login page

# Home page for logged in users
@login_required
def home_view(request):
    """
    Displays the home page, accessible only to logged-in users.
    """
    return render(request, 'home.html') # Use the main home.html template

# Simple view to render the signup page (can be used for GET requests to signup URL)
def signup_page(request):
    """
    Simply renders the signup template with an empty form for GET requests.
    This can be useful if you have a separate URL for just displaying the signup form.
    """
    form = CustomUserCreationForm() # Create an empty form
    return render(request, 'signup.html', {'form': form}) # Use the main signup.html template

def index(request):
    return render(request, 'index.html')
