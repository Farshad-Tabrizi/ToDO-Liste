from django.urls import path
from .views import TaskListView, TaskDetail, TaskCreateView, TaskUpdateView, TaskDeleteView, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('task-create/', TaskCreateView.as_view(), name='task-create'),
    path('login/', CustomLoginView.as_view(), name='login'),
   # path('logout/', LogoutView.as_view(next_page='login'), name="logout"),
    path('register/', RegisterPage.as_view(), name='register'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
    path('task-update/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
]