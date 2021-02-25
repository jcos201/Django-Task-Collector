from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('tasks/', views.tasks_index, name='index'),
    path('tasks/<int:task_id>/', views.task_detail, name='detail'),
    path('tasks/create/', views.TaskCreate.as_view(), name='tasks_create'),
    path('tasks/<int:pk>/update/', views.TaskUpdate.as_view(), name='tasks_update'),
    path('tasks/<int:pk>/delete/', views.TaskDelete.as_view(), name='tasks_delete'),
    path('tasks/<int:task_id>/status_update/', views.status_update, name='status_update'),
    path('tasks/<int:task_id>/assoc_team_members/<int:team_member_id>/', views.assoc_team_members, name='assoc_team_members'),
    path('tasks/<int:task_id>/remove_team_members/<int:team_member_id>/', views.remove_team_members, name='remove_team_members'),
    # Team Member URLs
    path('team_members/', views.TeamList.as_view(), name='team_index'),
    path('team_members/<int:pk>/', views.TeamDetail.as_view(), name='team_detail'),
    path('team_members/create/', views.TeamCreate.as_view(), name='team_create'),
    path('team_members/<int:pk>/update/', views.TeamUpdate.as_view(), name='team_update'),
    path('team_members/<int:pk>/delete/', views.TeamDelete.as_view(), name='team_delete'),
]