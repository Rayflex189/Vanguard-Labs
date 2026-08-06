# proposals/models.py
from django.db import models
from clients.models import Client
from portfolio.models import Project

class Proposal(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('draft','Draft'), ('sent','Sent'), ('accepted','Accepted'), ('rejected','Rejected')], default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Proposal for {self.client.name} - {self.title}"
