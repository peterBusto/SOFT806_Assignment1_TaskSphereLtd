from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.utils import timezone
import secrets
import hashlib

User = get_user_model()

class SimpleTokenAuthentication(BaseAuthentication):
    """
    Simple token authentication using API tokens
    """
    
    def authenticate(self, request):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
            
        # Extract token from "Token <token>" format
        if auth_header.startswith('Token '):
            token = auth_header[6:]  # Remove "Token " prefix
        else:
            token = auth_header
            
        if not token:
            return None
            
        # Validate token (simple implementation)
        try:
            # For this demo, we'll use a simple token validation
            # In production, store tokens in database with expiry
            user_id = self._validate_token(token)
            if not user_id:
                raise AuthenticationFailed('Invalid token')
                
            user = User.objects.get(id=user_id)
            return (user, token)
            
        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid token')
        except Exception:
            raise AuthenticationFailed('Token validation failed')
    
    def _validate_token(self, token):
        """
        Simple token validation - in production, use database lookup
        """
        # This is a simple demo implementation
        # In production, store tokens in database with user_id and expiry
        try:
            # For demo purposes, we'll decode a simple token format
            # Format: user_id_timestamp_hash
            parts = token.split('_')
            if len(parts) != 3:
                return None
                
            user_id = int(parts[0])
            timestamp = int(parts[1])
            hash_part = parts[2]
            
            # Check if token is not too old (24 hours)
            token_age = timezone.now().timestamp() - timestamp
            if token_age > 86400:  # 24 hours
                return None
                
            # Verify hash (simple validation)
            expected_hash = hashlib.md5(f"{user_id}_{timestamp}_secret".encode()).hexdigest()[:8]
            if hash_part != expected_hash:
                return None
                
            return user_id
            
        except:
            return None


def generate_token_for_user(user):
    """
    Generate a simple token for a user
    """
    timestamp = int(timezone.now().timestamp())
    hash_part = hashlib.md5(f"{user.id}_{timestamp}_secret".encode()).hexdigest()[:8]
    token = f"{user.id}_{timestamp}_{hash_part}"
    return token
