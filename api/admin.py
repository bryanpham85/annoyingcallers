from django.contrib import admin
from api.models import Caller, Category, Registered_Device

class Registered_DeviceAdmin(admin.ModelAdmin):
	list_display = ('deviceId', 'devicePlatform', 'status', 'installed_date')
	fields = ('deviceId', 'devicePlatform', 'status')

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'category_type', 'created_date')
	fields = ('name', 'category_type')

class CallerAdmin(admin.ModelAdmin):
	list_display = ('callerId', 'country_code', 'caller_number', 
		'categories', 'registered_date', 'registered_device')
	fields = ('country_code', 'caller_number', 'registered_device')
	# inlines = [CategoryInline,]

	def categories(self, obj):
		return '\n'.join([cat.name for cat in obj.category.all()])

	categories.short_description = "Category"
	def registered_device(self, obj):
		return '\n'.join(obj.registered_by.deviceId)
	registered_device.short_description = "DeviceId"

admin.site.register(Registered_Device, Registered_DeviceAdmin)
admin.site.register(Caller, CallerAdmin)
admin.site.register(Category, CategoryAdmin)