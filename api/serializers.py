from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id', 'username', 'email')

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_by = UserSerializer(read_only=True)
    class Meta:
        model=Task
        fields=(
            'id',
            'title',
            'description',
            'completed',
            'assigned_by',
            'assigned_to',
            'created_at',
            'completed_at',
            'deadline'
        )
class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields=(
            'title',
            'description',
            'deadline'
        )
    
        
class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields=(
            'title',
            'description',
            'completed',
            'deadline',
        )

# class TaskCreateSerializer(serializers.ModelSerializer):
#     assigned_to_id=serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(), source='assigned_to', write_only=True
#     )
#     class Meta:
#         model=Task
#         fields=(
#             'title',
#             'description',
#             'assigned_to_id',
#             'deadline'
#         )
# 
# class TaskSerializer(serializers.ModelSerializer):
#     assigned_to = UserSerializer(read_only=True)
#     assigned_by = UserSerializer(read_only=True)
#     assigned_to_id=serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(), source='assigned_to', write_only=True
#     )
#     class Meta:
#         model=Task
#         fields=(
#             'id',
#             'title',
#             'description',
#             'completed',
#             'assigned_by',
#             'assigned_to',
#             'assigned_to_id',
#             'created_at',
#             'completed_at',
#             'deadline'
#         )