from django.contrib import admin
from api.models import Caller, Category, Device, Caller_Category

class DeviceAdmin(admin.ModelAdmin):
	list_display = ('deviceId', 'devicePlatform', 'status', 'installed_date')
	fields = ('deviceId', 'devicePlatform', 'status')

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'description', 'created_date')
	fields = ('name', 'description')

class Caller_CategoryInline(admin.TabularInline):
	model = Caller_Category

class CallerAdmin(admin.ModelAdmin):
	list_display = ('callerId', 'country_code', 'caller_number', 'registered_date', 'registered_by_device')
	fields = ('country_code', 'caller_number', 'registered_by_device')
	inlines = (Caller_CategoryInline,)



	def categories(self, obj):
		return '\n'.join([cat.name for cat in obj.category.all()])

	categories.short_description = "Category"
	def registered_device(self, obj):
		return '\n'.join(obj.registered_by_device.deviceId)
	registered_device.short_description = "DeviceId"

admin.site.register(Device, DeviceAdmin)
admin.site.register(Caller, CallerAdmin)
admin.site.register(Category, CategoryAdmin)