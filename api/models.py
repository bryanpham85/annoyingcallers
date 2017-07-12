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

	STATUS = (
		(1, 'Active'),
		(0, 'Inactive'),
		)
	deviceId = models.CharField(max_length=100, primary_key=True) #UUID or AID of device
	devicePlatform = models.CharField(max_length=20, choices=PLATFORM)
	owner = models.ForeignKey(User, null=True) ## App can be use with annonymous mode
	status = models.IntegerField(null=False, default=1, choices=STATUS) #0 deactive, 1 active
	installed_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = ('ac_registered_device')
		ordering = ('installed_date',)


	def __str__(self):
		return self.deviceId


class Category(models.Model):
	"""
	Global used cross platform
	"""
	CATEGORY_TYPE = (
			(1, 'Private'),
			(2, 'Global'),
		)
	name = models.CharField(max_length=100, null=False, unique=True)
	category_type = models.IntegerField(null=False, choices=CATEGORY_TYPE)
	created_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = ('ac_category')
		ordering = ('created_date',)

	def __str__(self):
		return self.name



class Caller(models.Model):
	"""
	Description: a phone number is a caller at global of app
	"""
	COUNTRY_CODE = (
		('+84', 'VN(+84)'),
		('+1', 'US(+1)'),
	)
	callerId = models.AutoField(primary_key=True)
	country_code = models.CharField(max_length=5, choices=COUNTRY_CODE, null=False)
	caller_number = models.CharField(max_length = 11, null=False)
	registered_date = models.DateTimeField(auto_now_add=True)
	registered_device = models.ForeignKey('Registered_Device')
	category = models.ManyToManyField(Category)

	class Meta:
		db_table = ('ac_caller')
		ordering = ('registered_date',)
		indexes = [
			models.Index(fields=['country_code', 'caller_number'], name='caller_index')
		]

	def __str__(self):
		return str(self.callerId) + str(self.caller_number)

