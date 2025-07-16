from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerializer
from .models import Task
from django.shortcuts import get_object_or_404
from django.db.models import Q
# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    api_urls={
        'List':'/task-list/',
        'Detail View':'/task-detail/<str:pk>',
        'Create':'/task-create/',
        'Update':'/task-update/<str:pk>',
        'Delete':'/task-delete/<str:pk>',
        'Search':'/task-search/?q=your_query'
        }
    return Response(api_urls)


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