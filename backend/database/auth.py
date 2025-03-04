from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                # Check if user is suspended or inactive before allowing authentication
                if user.status in ['Suspended', 'Inactive']:
                    return None  # Return None to prevent login
                return user
        except User.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            # Also check status when getting user from session
            if user.status in ['Suspended', 'Inactive']:
                return None
            return user
        except User.DoesNotExist:
            return None 