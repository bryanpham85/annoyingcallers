from django.db import models
from django.contrib.auth.models import User


class Device(models.Model):
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
		db_table = ('ac_device')
		ordering = ('installed_date',)


	def __str__(self):
		return self.deviceId


class Category(models.Model):
	"""
	Global used cross platform
	"""
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100, null=False, unique=True)
	description = models.CharField(max_length=255, null=True)
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
		('VN', 'VN(+84)'),
		('US', 'US(+1)'),
	)
	callerId = models.AutoField(primary_key=True)
	country_code = models.CharField(max_length=5, choices=COUNTRY_CODE, null=False)
	caller_number = models.CharField(max_length = 11, null=False)
	registered_date = models.DateTimeField(auto_now_add=True)
	registered_by_device = models.ForeignKey('Device')
	category = models.ManyToManyField(Category, through="Caller_Category")

	class Meta:
		db_table = ('ac_caller')
		ordering = ('registered_date',)
		indexes = [
			models.Index(fields=['country_code', 'caller_number'], name='caller_index')
		]

	def __str__(self):
		return str(self.callerId) + str(self.caller_number)

class Caller_Category(models.Model):
	# to defferentiate betwen global and private category assignment
	ASSIGN_TYPE = (
			(1, 'Private'),
			(2, 'Global'),
		)
	caller_id = models.ForeignKey(Caller, on_delete=models.CASCADE)
	category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
	assign_type = models.IntegerField(null=False, choices=ASSIGN_TYPE)
	assigned_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table=('ac_caller_category')
		indexes = [
			models.Index(fields=['caller_id', 'category_id'], name='caller_category_index')
		]

