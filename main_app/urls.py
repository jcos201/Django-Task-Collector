from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('tasks/', views.tasks_index, name='index'),
    path('tasks/<int:task_id>/', views.task_detail, name='detail'),
    path('tasks/create/', views.TaskCreate.as_view(), name='tasks_create')
]