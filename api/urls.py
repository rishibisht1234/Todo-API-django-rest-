from django.urls import path
from . import views

urlpatterns = [
    path('',views.apiOverview,name='api-overview'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('task-list/',views.taskList,name='task-list'),
    path('task-detail/<str:pk>',views.taskDetail,name='task-detail'),
    path('task-create/',views.taskCreate,name='task-create'),
    path('task-update/<str:pk>',views.taskUpdate,name='task-update'),
    path('task-delete/<str:pk>',views.taskDelete,name='task-delete'),
    path('task-search/',views.taskSearch,name='task-search'),
]
