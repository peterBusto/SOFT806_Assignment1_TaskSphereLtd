from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .token_authentication import generate_token_for_user


@api_view(['POST'])
@permission_classes([AllowAny])
def token_login(request):
    """
    Token-based login - returns authentication token
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Username and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Authenticate user
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Generate token for the user
        token = generate_token_for_user(user)
        
        return Response({
            'message': 'Login successful',
            'token': token,
            'token_type': 'Token',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            },
            'expires_in': 86400  # 24 hours in seconds
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_token(request):
    """
    Verify if a token is valid
    """
    from .token_authentication import SimpleTokenAuthentication
    
    auth = SimpleTokenAuthentication()
    try:
        result = auth.authenticate(request)
        if result:
            user, token = result
            return Response({
                'valid': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            })
        else:
            return Response({
                'valid': False,
                'error': 'Invalid or missing token'
            }, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({
            'valid': False,
            'error': str(e)
        }, status=status.HTTP_401_UNAUTHORIZED)
