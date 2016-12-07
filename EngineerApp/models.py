from __future__ import unicode_literals

from django.db import models
from AuthenticationApp.models import MyUser
from CompaniesApp.models import Company

# Create your models here.

class Engineer(models.Model):
	engineer_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, unique=False)
	photo = models.ImageField(upload_to="static/engineerimages", default=0)
	email = models.CharField(max_length=300)
	user_map = models.OneToOneField(MyUser, on_delete=models.CASCADE, null=True, default=None)
	company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, default=None)

	def __str__(self):
		return self.name

