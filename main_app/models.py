from django.db import models
from django.urls import reverse

STATUS = (
    ('U', 'Unassigned'),
    ('N', 'Assigned - Not Done'),
    ('F', 'Assigned - Finished'),
)

# Create your models here.
class Team_Member(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=200)
    
    def __str__(self):
      return f'{self.name}'

    def get_absolute_url(self):
      return reverse('team_detail', kwargs={'pk': self.id})


class Task(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=250)
    due_date = models.DateField('due date')

    team_members = models.ManyToManyField(Team_Member)

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
      return reverse('detail', kwargs={'task_id': self.id})


class Status(models.Model):
    status = models.CharField(
      max_length=1,
      choices=STATUS,
      default=STATUS[0][0]
    )

    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
      return f"{self.get_status_display()}"
