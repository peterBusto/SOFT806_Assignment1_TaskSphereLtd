from django.contrib.sessions.models import Session
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from datetime import timedelta


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def session_info(request):
    """Get current session information including timeout"""
    session = request.session
    
    # Calculate session expiry
    expiry_time = session.get_expiry_date()
    time_remaining = expiry_time - timezone.now() if expiry_time else None
    
    return Response({
        'session_key': session.session_key,
        'expiry_date': expiry_time,
        'time_remaining_seconds': int(time_remaining.total_seconds()) if time_remaining else None,
        'is_expired': session.is_expired(),
        'age': session.get_age(),
        'timeout_setting': request.session.get_expiry_age()
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def extend_session(request):
    """Extend the current session timeout"""
    session = request.session
    
    # Extend session by the configured timeout period
    session.set_expiry(session.get_expiry_age())
    
    return Response({
        'message': 'Session extended successfully',
        'new_expiry_date': session.get_expiry_date(),
        'time_remaining_seconds': session.get_expiry_age()
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def logout_all_sessions(request):
    """Logout user from all devices/sessions"""
    # Delete all sessions for this user
    user_sessions = Session.objects.filter(
        session_data__contains=f'"_auth_user_id":{request.user.id}'
    )
    session_count = user_sessions.count()
    user_sessions.delete()
    
    return Response({
        'message': f'Logged out from {session_count} sessions',
        'sessions_terminated': session_count
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def active_sessions(request):
    """Get count of active sessions for current user"""
    user_sessions = Session.objects.filter(
        session_data__contains=f'"_auth_user_id":{request.user.id}'
    )
    
    sessions_info = []
    for session in user_sessions:
        try:
            expiry_time = session.expire_date
            time_remaining = expiry_time - timezone.now() if expiry_time else None
            sessions_info.append({
                'session_key': session.session_key[:10] + '...',  # Partial key for security
                'expiry_date': expiry_time,
                'time_remaining_seconds': int(time_remaining.total_seconds()) if time_remaining else None,
                'is_current': session.session_key == request.session.session_key
            })
        except:
            continue
    
    return Response({
        'active_sessions_count': len(sessions_info),
        'sessions': sessions_info
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def active_sessions(request):
    """Get count of active sessions for current user"""
    user_sessions = Session.objects.filter(
        session_data__contains=f'"_auth_user_id":{request.user.id}'
    )
    
    sessions_info = []
    for session in user_sessions:
        try:
            expiry_time = session.expire_date
            time_remaining = expiry_time - timezone.now() if expiry_time else None
            sessions_info.append({
                'session_key': session.session_key[:10] + '...',  # Partial key for security
                'expiry_date': expiry_time,
                'time_remaining_seconds': int(time_remaining.total_seconds()) if time_remaining else None,
                'is_current': session.session_key == request.session.session_key
            })
        except:
            continue
    
    return Response({
        'active_sessions_count': len(sessions_info),
        'sessions': sessions_info
    })
