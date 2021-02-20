from django.db import models

STATUS = (
    ('U', 'Unassigned'),
    ('N', 'Assigned - Not Done'),
    ('F', 'Assigned - Finished'),
)

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=250)
    status = models.CharField(
    max_length=1,
    choices=STATUS,
    default=STATUS[0][0]
  )

    def __str__(self):
        return f'{self.name}'