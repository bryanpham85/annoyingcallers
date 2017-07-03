from django.db import models
from django.contrib.auth.models import User


class Caller(models.Model):
	"""
	Description: a phone number is a caller at global of app
	"""
	COUNTRY_CODE = (
		('VN(+84)', '+84'),
	)
	callerId = models.AutoField(primary_key=True)
	country_code = models.CharField(max_length = 5, choices=COUNTRY_CODE, null=False)
	caller_number = models.CharField(max_length = 11, null=False)
	registerred_date = models.DateTimeField(auto_now_add=True)
	registerred_by = models.ForeignKey('Device')

	class Meta:
		ordering = ('registerred_date',)

class Device(models.Model):
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
	owner = models.ForeignKey(User, blank=True) ## App can be use with annonymous mode
	installed_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('installed_date',)

