from __future__ import unicode_literals

from django.db import models
#from ProjectsApp.models import Project
# Create your models here.

class Bookmark(models.Model):
	email = models.CharField(max_length=300)
	project = models.CharField(max_length=300)
	created_at = models.DateTimeField('date created', auto_now=True)

	def __str__(self):
		return self.name
