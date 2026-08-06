# crm/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=50, choices=[('new','New'), ('contacted','Contacted'), ('won','Won'), ('lost','Lost')], default='new')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
