from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
	"""
	Global used cross platform
	"""
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100, null=False, unique=True)
	description = models.CharField(max_length=255, null=True)
	created_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'ac_category'
		ordering = ('created_date',)
		app_label = 'api'

	def __str__(self):
		return self.name
