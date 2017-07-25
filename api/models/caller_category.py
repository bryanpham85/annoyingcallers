from django.db import models
from .category import Category
from .caller import Caller

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

		app_label = 'api'