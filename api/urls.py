from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet, UserViewSet
from .auth_views import RegisterView, LoginView, LogoutView, UserProfileView, current_user
from .session_views import session_info, extend_session, logout_all_sessions, active_sessions
from .test_views import test_public, test_protected, test_login_simple

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
    path('auth/me/', current_user, name='current-user'),
    # Session management endpoints
    path('session/info/', session_info, name='session-info'),
    path('session/extend/', extend_session, name='extend-session'),
    path('session/logout-all/', logout_all_sessions, name='logout-all-sessions'),
    path('session/active/', active_sessions, name='active-sessions'),
    # Test endpoints
    path('test/public/', test_public, name='test-public'),
    path('test/protected/', test_protected, name='test-protected'),
    path('test/login-simple/', test_login_simple, name='test-login-simple'),
]
