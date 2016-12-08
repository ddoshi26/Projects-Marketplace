from __future__ import unicode_literals

from django.db import models
from GroupsApp.models import Group


class Comment(models.Model):
    time = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=500)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, default=None)
    cname = models.CharField(max_length=50, unique=False, default=None)
    cemail = models.CharField(max_length=300, default=None)
