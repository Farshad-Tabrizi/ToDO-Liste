from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Task
class TaskListView(ListView):
    model = Task
    context_object_name = 'task'
class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/task.html'
class TaskCreateView(CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy('task-list')
