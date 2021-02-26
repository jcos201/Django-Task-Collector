from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
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
    team_members_not_assigned = Team_Member.objects.exclude(id__in = task.team_members.all().values_list('id'))
    status_form = StatusForm()
    return render(request, 'tasks/detail.html', { 
        'task':task, 
        'status_form':status_form,
        'available_team_members': team_members_not_assigned
     })

def assoc_team_members(request, task_id, team_member_id):
    Task.objects.get(id=task_id).team_members.add(team_member_id)
    return redirect('detail', task_id=task_id)

def remove_team_members(request, task_id, team_member_id):
    Task.objects.get(id=task_id).team_members.remove(team_member_id)
    return redirect('detail', task_id=task_id)

def status_update(request, task_id):
    form = StatusForm(request.POST)
    s = Task.objects.get(id=task_id).status_set.first()
    if form.is_valid():
        updated_status = form.cleaned_data['status']
        Status.objects.filter(pk=s.id).update(status=updated_status)
    return redirect('detail', task_id=task_id)

class TeamList(ListView):
    model = Team_Member

class TeamDetail(DetailView):
    model = Team_Member

class TeamCreate(CreateView):
    model = Team_Member
    fields = '__all__'

class TeamUpdate(UpdateView):
    model = Team_Member
    fields = '__all__'

class TeamDelete(DeleteView):
    model = Team_Member
    success_url = '/team_members/'

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