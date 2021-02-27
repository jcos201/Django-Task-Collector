from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

# Imports for creating User Signup Page
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Imports login_required decorator for custom defined views
from django.contrib.auth.decorators import login_required

# Imports LoginRequiredMixin for class based views
from django.contrib.auth.mixins import LoginRequiredMixin

# Import Custom Models
from .models import Task, Status, Team_Member, Photo

from .forms import StatusForm

# import for S3 photo upload
import uuid
import boto3

# Constants for S3 photo upload
S3_BASE_URL='https://S3.us-east-1.amazonaws.com/'
BUCKET = 'taskcollector'

# Create your views here.
from django.http import HttpResponse

def signup(request):
    error_message = ''
    if request.method == 'POST':
        #If signup filled form has been submited run the folowing code
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # If the form has been filled out correctly create the user
            user = form.save()
            # This will login in the user so they don't have to re-login after signup
            login(request,user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up, please try again'
    # If request.method was abad POST or a GET request, render signup.html with empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['name','description','due_date']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    status_form = StatusForm()
    fields = ['description', 'due_date']

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = '/tasks/'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def tasks_index(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/index.html', { 'tasks': tasks })

@login_required
def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    user_team = Team_Member.objects.filter(user=request.user)
    if task.status_set.count() == 0:
        Status.objects.create(status='U',task=task)
    team_members_not_assigned = user_team.exclude(id__in = task.team_members.all().values_list('id'))
    status_form = StatusForm()
    return render(request, 'tasks/detail.html', { 
        'task':task, 
        'status_form':status_form,
        'available_team_members': team_members_not_assigned
     })

@login_required
def assoc_team_members(request, task_id, team_member_id):
    Task.objects.get(id=task_id).team_members.add(team_member_id)
    return redirect('detail', task_id=task_id)

@login_required
def remove_team_members(request, task_id, team_member_id):
    Task.objects.get(id=task_id).team_members.remove(team_member_id)
    return redirect('detail', task_id=task_id)

@login_required
def status_update(request, task_id):
    form = StatusForm(request.POST)
    s = Task.objects.get(id=task_id).status_set.first()
    if form.is_valid():
        updated_status = form.cleaned_data['status']
        Status.objects.filter(pk=s.id).update(status=updated_status)
    return redirect('detail', task_id=task_id)


#class TeamList(LoginRequiredMixin, ListView):
#    model = Team_Member

@login_required
def team_list(request):
    team = Team_Member.objects.filter(user=request.user)
    return render(request, 'main_app/team_member_list.html', { 'team_member_list': team })

class TeamDetail(LoginRequiredMixin, DetailView):
   model = Team_Member

class TeamCreate(LoginRequiredMixin, CreateView):
    model = Team_Member
    fields = ['name','role']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TeamUpdate(LoginRequiredMixin, UpdateView):
    model = Team_Member
    fields = ['name','role']

class TeamDelete(LoginRequiredMixin, DeleteView):
    model = Team_Member
    success_url = '/team_members/'

@login_required
def add_photo(request, team_member_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # The next line of code creates a unique 'key' for S3 and adds file extension with +
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # The next line of code builds the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # If Team Member already has photo, replace the photo with the new updated one
            tm = Team_Member.objects.get(id=team_member_id)
            if tm.photo_set.count():
                current_photo = tm.photo_set.first()
                Photo.objects.filter(id=current_photo.id).update(url=url)
            else:
                photo = Photo(url=url, team_member_id=team_member_id)
                photo.save()
        except:
            print('An error occured uploading file to S3')
    return redirect('/team_members', team_member_id=team_member_id)