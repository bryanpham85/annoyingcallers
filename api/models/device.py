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
	api_request_key = models.CharField(max_length=255, null=False)
	installed_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = ('ac_device')
		ordering = ('installed_date',)
		app_label = 'api'


	def __str__(self):
		return self.deviceId
