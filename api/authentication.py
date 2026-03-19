from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.contrib.sessions.models import Session
from django.utils import timezone


class CSRFExemptSessionAuthentication(SessionAuthentication):
    """
    Custom session authentication that bypasses CSRF validation
    """
    def enforce_csrf(self, request):
        # Override to bypass CSRF validation
        return
    
    def authenticate(self, request):
        """
        Authenticates the request and returns a two-tuple of (user, token).
        """
        # Get the session from the request
        session = request.session
        
        # Check if the session has a user ID
        user_id = session.get('_auth_user_id')
        if not user_id:
            return None
        
        # Get the user from the session
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(id=user_id)
            
            # Check if the session is still valid
            if session.is_expired():
                return None
                
            return (user, None)
        except:
            return None
