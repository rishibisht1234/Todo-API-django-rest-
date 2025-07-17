from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerializer
from .models import Task
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    api_urls={
        'Register':'/register/',
        'Login':'/login/',
        'List':'/task-list/',
        'Detail View':'/task-detail/<str:pk>',
        'Create':'/task-create/',
        'Update':'/task-update/<str:pk>',
        'Delete':'/task-delete/<str:pk>',
        'Search':'/task-search/?q=your_query'
        }
    return Response(api_urls)

@api_view(['POST'])
def register(request):
    username=request.data.get('username')
    password=request.data.get('password')
    if not username or not password:
        return Response({'error':"username and password are required"},status=400)
    if User.objects.filter(username=username).exists():
        return Response({'error':'username already exists'},status=400)
    
    user=User.objects.create_user(username=username,password=password)
    token= Token.objects.create(user=user)
    return Response({'token':token.key},status=201)

@api_view(['POST'])
def login(request):
    username=request.data.get('username')
    password=request.data.get('password')
    user=authenticate(username=username,password=password)
    if user is None:
        return Response({'error':"Invalid credentials"},status=400)
    token,created=Token.objects.get_or_create(user=user)
    return Response({'token':token.key},status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({'message':"Successfully logged out"},status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def taskList(request):
    tasks=Task.objects.filter(Q(assigned_by=request.user) | Q(assigned_to=request.user)).order_by('-created_at')
    serializer=TaskSerializer(tasks,many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def taskDetail(request,pk):
    task=get_object_or_404(Task,pk=pk)
    if request.user != task.assigned_by and request.user!= task.assigned_to:
        return Response({'error': 'You do not have permission to view this task.'}, status=403)
    
    serializer=TaskSerializer(task)
    return Response(serializer.data)

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def taskCreate(request):
    serializer=TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(assigned_by=request.user)
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors,status=400)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def taskUpdate(request,pk):
    task=get_object_or_404(Task,pk=pk)
    if request.user != task.assigned_by:
        return Response({'error': 'You do not have permission to update this task.'}, status=403)
    
    serializer=TaskSerializer(instance=task,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=200)
    else:
        return Response(serializer.errors,status=400)
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def taskDelete(request,pk):
    task=get_object_or_404(Task,pk=pk)
    if request.user != task.assigned_by:
        return Response({'error': 'You do not have permission to delete this task.'}, status=403)
    
    task.delete()
    return Response({'message':"Item Successfully deleted!!"},status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def taskSearch(request):
    query=request.GET.get('q','')
    tasks=Task.objects.filter(Q(title__icontains=query)|
                              Q(description__icontains=query))
    tasks=tasks.filter(Q(assigned_by=request.user) | Q(assigned_to=request.user)).order_by('-created_at')
    serializer=TaskSerializer(tasks,many=True)
    return Response(serializer.data)

