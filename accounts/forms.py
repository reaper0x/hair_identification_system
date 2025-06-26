from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth import authenticate # Import authenticate for custom cleaning
from django.contrib.auth import get_user_model # Import get_user_model

User = get_user_model() # Get the currently active user model

class EmailAuthenticationForm(AuthenticationForm):
    """
    A custom authentication form that uses email instead of username for login.
    """
    # Override the default 'username' field to be an EmailInput and label it 'Email'
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'id': 'id_email',
            'placeholder': 'you@example.com',
            'required': True,
            'autofocus': True,
            'aria-required': 'true',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500' # Tailwind classes
        })
    )
    
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'id': 'id_password',
            'placeholder': 'Enter your password',
            'required': True,
            'aria-required': 'true',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500' # Tailwind classes
        })
    )

    def clean(self):
        """
        Custom clean method to authenticate user based on email and password.
        """
        email = self.cleaned_data.get('username') # 'username' field now holds email
        password = self.cleaned_data.get('password')

        if email and password:
            # Use authenticate to verify credentials. This checks against the configured auth backend.
            # Note: authenticate typically looks for 'username', so ensure your User model
            # allows email as a username or use a custom authentication backend.
            self.user_cache = authenticate(self.request, username=email, password=password)
            
            if self.user_cache is None:
                # Raise a validation error if authentication fails
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name}, # Use verbose_name (which is 'Email')
                )
            else:
                # Ensure the user is allowed to log in (e.g., not disabled)
                self.confirm_login_allowed(self.user_cache)
        
        return self.cleaned_data

class CustomUserCreationForm(UserCreationForm):
    """
    A custom user creation form that includes an email field.
    """
    email = forms.EmailField(
        label="Email",
        max_length=254,
        help_text="Required. Enter a valid email address.",
        widget=forms.EmailInput(attrs={
            'id': 'id_email_signup',
            'placeholder': 'you@example.com',
            'required': True,
            'aria-required': 'true',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500' # Tailwind classes
        })
    )
    username = forms.CharField(
        label="Username",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'id_username_signup',
            'placeholder': 'Username',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500' # Tailwind classes
        })
    )

    class Meta(UserCreationForm.Meta): # Inherit Meta from UserCreationForm for default fields
        model = User
        fields = ("username", "email") # Explicitly list fields, 'password' is handled by UserCreationForm itself

    def clean_email(self):
        """
        Custom cleaning for email to ensure uniqueness.
        """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def clean_username(self):
        """
        Custom cleaning for username. Allows duplicate usernames.
        """
        return self.cleaned_data['username']

    def clean_password2(self):
        """
        Custom cleaning for the password confirmation field.
        Checks if the two password entries match and if the password is strong enough.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn’t match.")
        # Use Django's built-in password validators
        from django.contrib.auth.password_validation import validate_password
        try:
            validate_password(password1)
        except forms.ValidationError:
            raise forms.ValidationError("Password too weak.")
        return password2

    def save(self, commit=True):
        """
        Overrides save to ensure email is saved with the user.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

