"""ProjectsApp Models

Created by Harris Christiansen on 10/02/16.
"""
from django.db import models
from AuthenticationApp.models import MyUser
from GroupsApp.models import Group
from CompaniesApp.models import Company

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)
    created_by = models.ForeignKey(MyUser, null=True, default=None,) 
    programming_language = models.CharField(max_length=100, default=None)
    experience = models.CharField(max_length=3, default=None)
    skills = models.CharField(max_length=200, default=None)
    group = models.OneToOneField(Group, null=True, default=None)
    company = models.ForeignKey(Company, null=True, default=None)

    def __str__(self):
        return self.name
