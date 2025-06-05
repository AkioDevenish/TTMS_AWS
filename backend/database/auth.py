from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import exceptions
from django.utils import timezone
from .models import ApiAccessKey, ApiKeyUsageLog

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

class ApiKeyAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication class for API key based authentication
    """
    def authenticate(self, request):
        # Try getting API key from X-API-Key header
        api_key = request.META.get('HTTP_X_API_KEY')
        
        # If not found, try Authorization: Bearer header
        if not api_key and 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2 and auth[0].lower() == 'bearer':
                api_key = auth[1]
        
        # If no API key provided, don't attempt to authenticate
        if not api_key:
            return None
            
        try:
            # Find the key in the database
            access_key = ApiAccessKey.objects.get(uuid=api_key)
            
            # Check if key has expired
            if access_key.expires_at and access_key.expires_at < timezone.now():
                raise exceptions.AuthenticationFailed('API key has expired')
                
            # Store the entire API key object (not just the token string)
            # This is what the view will check for
            user = access_key.user
            user.auth_token = access_key
            
            # Return user and token for authentication
            return (user, access_key)
            
        except ApiAccessKey.DoesNotExist:
            # If the key doesn't exist, authentication failed for API key, return None
            return None
        except exceptions.AuthenticationFailed as e:
            # If ApiKeyAuthentication explicitly raised AuthenticationFailed (e.g. expired), let it propagate
            raise e
        except Exception as e:
            # For any other exception during API key processing, treat as API key failure and return None
            print(f"Error during API key authentication: {str(e)}")
            return None 