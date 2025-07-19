from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import Task
from django.db.models import Q
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
# Create your views here.
# Class Based View
from rest_framework import generics
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema,OpenApiRequest, OpenApiResponse, inline_serializer,OpenApiParameter
from rest_framework import serializers


class RegisterView(APIView):
    @extend_schema(
        request=inline_serializer(
            name='RegisterRequest',
            fields={
                'username':serializers.CharField(),
                'password':serializers.CharField(write_only=True),
                'email':serializers.EmailField(required=False)
            }
        ),
        responses=inline_serializer(
            name='RegisterResponse',
            fields={
                'id':serializers.IntegerField(),
                'username': serializers.CharField(),
                'email': serializers.EmailField(),
                'token': serializers.CharField()
            }
        ),
        description="Register a new user and receive authentication token",
    )  
    def post(self, request):
        username=self.request.data.get('username')
        password=self.request.data.get('password')
        email=self.request.data.get('email', None)
        if not username or not password:
            return Response({'error':"username and password are required"},status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error':'username already exists'},status=status.HTTP_400_BAD_REQUEST)
        user=User.objects.create_user(username=username,password=password,email=email)
        token=Token.objects.create(user=user)
        return Response({
            'id':user.id,
            'username':user.username,
            'email':user.email,
            'token':token.key},
            status=status.HTTP_201_CREATED)
        
    

class LoginView(APIView):
    @extend_schema(
        request=inline_serializer(
            name='LoginRequest',
            fields={
                'username': serializers.CharField(),
                'password': serializers.CharField(),
            }
        ),
        responses=inline_serializer(
            name='LoginResponse',
            fields={
                'token': serializers.CharField(),
                'username': serializers.CharField(),
                'email': serializers.EmailField(),
                'id': serializers.IntegerField()
            }
        ),
        description="Login and receive authentication token"
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'detail': 'Username and password are required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if not user:
            return Response({'detail': 'Invalid credentials.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'id': user.id,
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        description="Logout the user and delete the authentication token",
        responses=inline_serializer(
            name="logoutResponse",
            fields={
                "message":serializers.CharField()
            }
        )
    )
    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': "Successfully logged out"}, status=status.HTTP_200_OK)



class TaskListView(generics.ListAPIView):
    queryset=Task.objects.all()
    serializer_class=TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(Q(assigned_by=self.request.user) |
                        Q(assigned_to=self.request.user)).order_by('-created_at')



class TaskDetailView(generics.RetrieveAPIView):
    queryset= Task.objects.all()
    serializer_class=TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs=super().get_queryset()
        return qs.filter(Q(assigned_by=self.request.user) |
                                   Q(assigned_to=self.request.user))

class TaskCreateView(generics.CreateAPIView):
    model= Task
    serializer_class=TaskCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user,assigned_to=self.request.user)
        
class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(Q(assigned_by=self.request.user) |
                         Q(assigned_to=self.request.user))

class CompleteTaskToggleView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Toggle a task's completion",
        responses=inline_serializer(
            name="CompleteTaskToggleResponse",
            fields={
                "message": serializers.CharField(),
                "task_id": serializers.IntegerField(),
                "completed": serializers.BooleanField(),
            }
        )
    )
    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        user=request.user
        if task.assigned_to != user and task.assigned_by != user:
            return Response(
                {"message": "You are not authorized to modify this task."},
                status=status.HTTP_403_FORBIDDEN
            )

        task.completed = not task.completed
        task.save()

        return Response({
            "message": "Complete status changed",
            "task_id": task.id,
            "completed": task.completed
        }, status=status.HTTP_200_OK)
        
class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(assigned_by=self.request.user)


@extend_schema(
    parameters=[
        OpenApiParameter(name='q', type=str, description='Search query')
    ],
)
class TaskSearchView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        qs = Task.objects.filter(Q(title__icontains=query) |
                                 Q(description__icontains=query))
        return qs.filter(Q(assigned_by=self.request.user) |
                         Q(assigned_to=self.request.user)).order_by('-created_at')

class UsernameIdMappingView(APIView):
    permission_classes=[IsAuthenticated]
    
    @extend_schema(
        description="Get all User's id, username and email",
        responses=inline_serializer(
            name="Userlist",
            fields={
                "id": serializers.IntegerField(),
                "username": serializers.CharField(),
                "email": serializers.EmailField(),
            }
        )
    )
    def get(self,request):
        users=User.objects.all()
        serializers=UserSerializer(users,many=True)
        return Response(serializers.data)
            




# from django.shortcuts import render
# from django.http import JsonResponse
# from rest_framework.response import Response
# from rest_framework.decorators import api_view,permission_classes
# from rest_framework.permissions import IsAuthenticated
# from .serializers import TaskSerializer
# from .models import Task
# from django.shortcuts import get_object_or_404
# from django.db.models import Q
# from rest_framework import status
# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
# from django.contrib.auth import authenticate
# # Create your views here.

# @api_view(['GET'])
# def apiOverview(request):
#     api_urls={
#         'Register':'/register/',
#         'Login':'/login/',
#         'List':'/task-list/',
#         'Detail View':'/task-detail/<str:pk>',
#         'Create':'/task-create/',
#         'Update':'/task-update/<str:pk>',
#         'Delete':'/task-delete/<str:pk>',
#         'Search':'/task-search/?q=your_query'
#         }
#     return Response(api_urls)

# @api_view(['POST'])
# def register(request):
#     username=request.data.get('username')
#     password=request.data.get('password')
#     if not username or not password:
#         return Response({'error':"username and password are required"},status=400)
#     if User.objects.filter(username=username).exists():
#         return Response({'error':'username already exists'},status=400)
    
#     user=User.objects.create_user(username=username,password=password)
#     token= Token.objects.create(user=user)
#     return Response({'token':token.key},status=201)

# @api_view(['POST'])
# def login(request):
#     username=request.data.get('username')
#     password=request.data.get('password')
#     user=authenticate(username=username,password=password)
#     if user is None:
#         return Response({'error':"Invalid credentials"},status=400)
#     token,created=Token.objects.get_or_create(user=user)
#     return Response({'token':token.key},status=200)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def logout(request):
#     request.user.auth_token.delete()
#     return Response({'message':"Successfully logged out"},status=200)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def taskList(request):
#     tasks=Task.objects.filter(Q(assigned_by=request.user) | Q(assigned_to=request.user)).order_by('-created_at')
#     serializer=TaskSerializer(tasks,many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def taskDetail(request,pk):
#     task=get_object_or_404(Task,pk=pk)
#     if request.user != task.assigned_by and request.user!= task.assigned_to:
#         return Response({'error': 'You do not have permission to view this task.'}, status=403)
    
#     serializer=TaskSerializer(task)
#     return Response(serializer.data)

    
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])  
# def taskCreate(request):
#     serializer=TaskSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(assigned_by=request.user)
#         return Response(serializer.data, status=201)
#     else:
#         return Response(serializer.errors,status=400)
    

# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def taskUpdate(request,pk):
#     task=get_object_or_404(Task,pk=pk)
#     if request.user != task.assigned_by:
#         return Response({'error': 'You do not have permission to update this task.'}, status=403)
    
#     serializer=TaskSerializer(instance=task,data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data,status=200)
#     else:
#         return Response(serializer.errors,status=400)
    

# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def taskDelete(request,pk):
#     task=get_object_or_404(Task,pk=pk)
#     if request.user != task.assigned_by:
#         return Response({'error': 'You do not have permission to delete this task.'}, status=403)
    
#     task.delete()
#     return Response({'message':"Item Successfully deleted!!"},status=200)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def taskSearch(request):
#     query=request.GET.get('q','')
#     tasks=Task.objects.filter(Q(title__icontains=query)|
#                               Q(description__icontains=query))
#     tasks=tasks.filter(Q(assigned_by=request.user) | Q(assigned_to=request.user)).order_by('-created_at')
#     serializer=TaskSerializer(tasks,many=True)
#     return Response(serializer.data)

