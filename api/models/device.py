from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

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
	id = models.CharField(max_length=100, primary_key=True) #UUID or AID of device
	platform = models.CharField(max_length=20, choices=PLATFORM)
	owner = models.ForeignKey(User, null=True) ## App can be use with annonymous mode
	status = models.IntegerField(null=False, default=1, choices=STATUS) #0 deactive, 1 active
	api_request_key = models.CharField(max_length=255, null=False)
	installed_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'ac_device'
		ordering = ('installed_date',)
		app_label = 'api'


	def __str__(self):
		return self.id

	#Overwrite the model.clean_field -> clean -> validate_unique
	def clean(self):
		if self.platform is None:
			raise ValidationError({
				'platform_not_null': _("platform cannot be none"),
			})

	def validate_unique(self):
		if super(Device, self).validate_unique(exclude=None) is not True:
			raise ValidationError({
				'unique_id': _('The device already exist. The new API_REQUEST_KEY already renew'),
			})
			return False
		return True
