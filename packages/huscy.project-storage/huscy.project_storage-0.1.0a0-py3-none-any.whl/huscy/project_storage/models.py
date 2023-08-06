from django.conf import settings
from django.db import models

from huscy.projects.models import Project


class StorageRequest(models.Model):
    safe_storage = models.PositiveSmallIntegerField(default=0)
    fast_storage = models.PositiveSmallIntegerField(default=0)
    note = models.TextField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    depositor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
