from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, Task, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'phone_number', 'timezone', 'company', 'position', 'is_verified']
        read_only_fields = ['is_verified']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm', 'profile']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        validated_data.pop('password_confirm')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        
        UserProfile.objects.create(user=user, **profile_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    tasks_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'is_completed', 
                  'created_at', 'updated_at', 'tasks_count']

    def get_tasks_count(self, obj):
        return obj.tasks.count()


class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'assigned_to', 'created_by',
                  'priority', 'priority_display', 'status', 'status_display', 
                  'created_at', 'updated_at', 'due_date']


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'assigned_to', 
                  'priority', 'status', 'due_date']

    def validate_project(self, value):
        if value.owner != self.context['request'].user:
            raise serializers.ValidationError("You can only create tasks in your own projects.")
        return value


class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'is_completed']
