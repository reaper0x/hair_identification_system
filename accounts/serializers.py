from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get('username', ''),  # Allow duplicate usernames
            email=validated_data['email'],
            password=validated_data['password']
        )
        from .utils import send_verification_email  # Import here to avoid circular import issues
        request = self.context.get('request')
        if request:
            send_verification_email(user, request)
        return user
