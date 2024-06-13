from django.urls import path
from .views import TaskListView, TaskDetail, TaskCreateView

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('task-create/', TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
]