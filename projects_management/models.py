# projects_management/models.py
from django.db import models
from portfolio.models import Project

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    assigned_to = models.ForeignKey('team.TeamMember', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.project.title} - {self.title}"
