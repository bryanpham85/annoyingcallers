from django.contrib import admin
# from api.models.device import Device
# from api.models.category import Category
# from api.models.caller import Caller
# from api.models.caller_category import Caller_Category 
from .models import *

class DeviceAdmin(admin.ModelAdmin):
	list_display = ('id', 'platform', 'status', 'api_request_key', 'installed_date')
	fields = ('id', 'platform', 'api_request_key', 'status')

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'description', 'created_date')
	fields = ('name', 'description')

class Caller_CategoryInline(admin.TabularInline):
	model = Caller_Category

class CallerAdmin(admin.ModelAdmin):
	list_display = ('id', 'country_code', 'number', 'registered_date', 'registered_by_device')
	fields = ('country_code', 'number', 'registered_by_device')
	inlines = (Caller_CategoryInline,)



	def categories(self, obj):
		return '\n'.join([cat.name for cat in obj.category.all()])

	categories.short_description = "Category"
	def registered_device(self, obj):
		return '\n'.join(obj.registered_by_device.id)
	registered_device.short_description = "DeviceId"

admin.site.register(Device, DeviceAdmin)
admin.site.register(Caller, CallerAdmin)
admin.site.register(Category, CategoryAdmin)