from django.db import models
from django.contrib.auth.models import User
from .category import Category
from .device import Device
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

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

		app_label = 'api'

	def __str__(self):
		return str(self.callerId) + str(self.caller_number)

	def clean(self):
		if self.caller_number is None or self.caller_number== '':
			raise ValidationError({'caller_number': _('Caller number cannot be empty')})
