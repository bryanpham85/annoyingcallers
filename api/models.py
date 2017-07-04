from django.db import models
from django.contrib.auth.models import User


class Registered_Device(models.Model):
	"""
	Devices install AnnoyingCaller app
	"""
	PLATFORM = (
		('Android', 'Android'),
		('iOS', 'iOS'),
		('Blackberry', 'Blackberry'),
	)
	deviceId = models.CharField(max_length=100, primary_key=True) #UUID or AID of device
	devicePlatform = models.CharField(max_length=20, choices=PLATFORM)
	owner = models.ForeignKey(User) ## App can be use with annonymous mode
	installed_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = ('ac_registered_device')
		ordering = ('installed_date',)

class Caller(models.Model):
	"""
	Description: a phone number is a caller at global of app
	"""
	COUNTRY_CODE = (
		('VN(+84)', '+84'),
	)
	callerId = models.AutoField(primary_key=True)
	country_code = models.CharField(max_length=5, choices=COUNTRY_CODE, null=False)
	caller_number = models.CharField(max_length = 11, null=False)
	registered_date = models.DateTimeField(auto_now_add=True)
	registered_by = models.ForeignKey('Registered_Device')

	class Meta:
		db_table = ('ac_caller')
		ordering = ('registered_date',)
		indexes = [
			models.Index(fields=['country_code', 'caller_number'], name='caller_index')
		]



class Category(models.Model):
	"""
	Global used cross platform
	"""
	CATEGORY_TYPE = (
			('Private', 1),
			('Global', 2),
		)
	name = models.CharField(max_length=100, null=False, unique=True)
	category_type = models.IntegerField(null=False, choices=CATEGORY_TYPE)
	created_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = ('ac_category')
		ordering = ('created_date',)

class Caller_Categories(models.Model):
	"""
	The caller marked into category by owner from device, this table only count the number of report time from community
	"""
	callerId = models.ForeignKey('Caller', null=False)
	categoryId = models.ForeignKey('Category', null=False)
	total_report_count = models.IntegerField(default=0)
	positive_sentiment_count = models.IntegerField(default=0)
	negative_sentiment_count = models.IntegerField(default=0)

	class Meta:
		db_table = ('ac_caller_category')
		index_together = ['callerId', 'categoryId']
