from django.db import models
from .category import Category

class Caller(models.Model):
	"""
	Description: a phone number is a caller at global of app
	"""
	COUNTRY_CODE = (
		('VN', 'VN(+84)'),
		('US', 'US(+1)'),
	)
	id = models.AutoField(primary_key=True)
	country_code = models.CharField(max_length=5, choices=COUNTRY_CODE, null=False)
	number = models.CharField(max_length = 11, null=False)
	registered_date = models.DateTimeField(auto_now_add=True)
	registered_by_device = models.ForeignKey('Device')
	category = models.ManyToManyField(Category, through="CallerCategory")

	class Meta:
		db_table = 'ac_caller'
		ordering = ('registered_date',)
		indexes = [
			models.Index(fields=['country_code', 'number'], name='caller_index')
		]

		app_label = 'api'

	def __str__(self):
		return str(self.id) + str(self.number)

