from django.urls import path
from .views import *


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/',ChangePassView.as_view(),name='change-password'),
    path('task-list/',TaskListView.as_view(),name='task-list'),
    path('task-detail/<str:pk>',TaskDetailView.as_view(),name='task-detail'),
    path('task-create/',TaskCreateView.as_view(),name='task-create'),
    path('task-update/<str:pk>',TaskUpdateView.as_view(),name='task-update'),
    path('task-toggle/<str:pk>',CompleteTaskToggleView.as_view(),name='task-complete-toggle'),
    path('task-delete/<str:pk>',TaskDeleteView.as_view(),name='task-delete'),
    path('task-search/',TaskSearchView.as_view(),name='task-search'),
    path("user-list/",UsernameIdMappingView.as_view(),name="user-list"),
]
