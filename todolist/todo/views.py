from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task

# Definition der Views für die To-Do-Listen-Anwendung
class TaskListView(LoginRequiredMixin, ListView):
    """
        ListView für die Anzeige der Liste von Aufgaben (Tasks) eines angemeldeten Benutzers.
        """
    model = Task
    context_object_name = 'task'

    def get_context_data(self, **kwargs):

        #Fügt zusätzliche Kontextdaten hinzu, speziell die Anzahl der unerledigten Aufgaben.

        context = super().get_context_data(**kwargs)
        context['task'] = context['task'].filter(user=self.request.user)
        context['count'] = context['task'].filter(completed=False).count()
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    #DetailView zur Anzeige der Details einer bestimmten Aufgabe (Task).

    model = Task
    context_object_name = 'task'
    template_name = 'todo/task.html'

class TaskCreateView(LoginRequiredMixin, CreateView):
    #CreateView zur Erstellung neuer Aufgaben (Tasks) durch angemeldete Benutzer.

    model = Task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        #Validiert das Formular und weist die aktuelle Benutzerinstanz der neuen Aufgabe zu.

        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    #UpdateView zur Aktualisierung von Aufgaben (Tasks) durch angemeldete Benutzer.

    model = Task
    fields = ['title', 'description', 'completed'] #__all__ -> {detaliert}
    success_url = reverse_lazy('task-list')

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    # DeleteView zum Löschen von Aufgaben (Tasks) durch angemeldete Benutzer.
    model = Task
    context_object_name = 'task-list'
    success_url = reverse_lazy('task-list')

class CustomLoginView(LoginView):
    # Anpassbare LoginView zur Authentifizierung von Benutzern.

    template_name = 'todo/login.html'
    fields = '__all__'
    redirect_authenticated_user = False

    def get_success_url(self):
        #Gibt die URL zurück, zu der der Benutzer nach erfolgreicher Anmeldung weitergeleitet wird.

        return reverse_lazy('task-list')


class RegisterPage(FormView):
    #FormView zur Registrierung neuer Benutzer mit dem Django UserCreationForm.

    template_name = 'todo/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        # Validiert das Registrierungsformular und meldet den Benutzer nach erfolgreicher Registrierung an.

        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)


