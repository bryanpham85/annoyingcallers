from django.contrib.auth.models import User, Group
from .models import Caller, Device, Category, CallerCategory
from rest_framework import serializers
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

##This is for global auth
class UserSerializer (serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'username', 'email', 'groups')

class GroupSerializer (serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ('url', 'name')



##Category Serializer - Just define for get because app will not create category
class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ('id', 'name', 'description', 'created_date')

class CallerCategorySerializer(serializers.ModelSerializer):
	id = serializers.ReadOnlyField(source='category.id')
	name = serializers.ReadOnlyField(source='category.name')

	class Meta:
		model = CallerCategory
		fields = ('id', 'name', 'assign_type', 'assigned_date')
#Device added when app install
### owner can be null in case of annonymous
class DeviceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Device
		fields = ('id', 'platform', 'owner', 'status', 'api_request_key')

	def create(self, validated_data):
		print("Ime in create devie")
		return Device.objects.create(**validated_data)


	def update(self, instance, validated_data):
		instance.owner = validated_data.get('owner', instance.owner)
		instance.status = validated_data.get('status', instance.status)
		#Validate the date and throw exception in case of violated.
		try:
			print("Validate Duplication of DeviceID")
			instance.full_clear()
		except ValidationError as e:
			non_field_errors = e.message_dict[NON_FIELD_ERRORS]
			return non_field_errors
		instance.save()
		return instance



#####Caller serializer
class CallerSerializer(serializers.ModelSerializer):
	#category = CategorySerializer(read_only=True, many=True)
	category = CallerCategorySerializer(read_only=True, many='true', source='callercategory_set')


	class Meta:
		model = Caller
		fields = ('id', 'country_code', 
			'number', 'category', 'registered_date', 'registered_by_device')

	def create(self, validated_data):
		"""
		Create and return a caller with validated data
		"""
		if validated_data['number'].startswith('0'):
			validated_data['number'] = validated_data['number'][1:]
		if validated_data['number'].startswith('+84'):
			validated_data['number'] = validated_data['number'][3:]

		return Caller.objects.create(**validated_data)

	def update(self, instance, validated_data):
		"""
		Update and return existing caller with validated data
		"""
		instance.country_code = validated_data.get('country_code',instance.country_code)
		instance.number = validated_data.get('number', instance.number)
		instance.save()
		return instance







