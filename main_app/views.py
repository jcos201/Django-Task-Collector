from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Task, Status

from .forms import StatusForm

# Create your views here.
from django.http import HttpResponse

class TaskCreate(CreateView):
    model = Task
    fields = '__all__'
    success_url = 'tasks/'

class TaskUpdate(UpdateView):
    model = Task
    status_form = StatusForm()
    fields = ['description', 'due_date']

class TaskDelete(DeleteView):
    model = Task
    success_url = '/tasks/'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def tasks_index(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/index.html', { 'tasks': tasks })

def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    status_form = StatusForm()
    return render(request, 'tasks/detail.html', { 'task':task, 'status_form':status_form })

def status_update(request, task_id):
    form = StatusForm(request.POST)
    s = Task.objects.get(id=task_id).status_set.first()
    if form.is_valid():
        updated_status = form.cleaned_data['status']
        Status.objects.filter(pk=s.id).update(status=updated_status)
    return redirect('detail', task_id=task_id)