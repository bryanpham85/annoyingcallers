from django.contrib.auth.models import User, Group
from api.models import Caller, Device, Category
from rest_framework import serializers
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
		fields = ('id', 'name', 'category_type', 'created_date')

#Registered_Device added when app install
### owner can be null in case of annonymous
class DeviceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Device
		fields = ('deviceId', 'devicePlatform', 'owner', 'status')

	def create(self, validated_data):
		return Device.objects.create(**validated_data)


	def update(self, instance, validated_data):
		instance.owner = validated_data.get('owner', instance.owner)
		instance.status = validated_data.get('status', instance.status)
		instance.save()
		return instance



#####Caller serializer
class CallerSerializer(serializers.ModelSerializer):
	category = CategorySerializer(read_only=True, many=True)

	class Meta:
		model = Caller
		fields = ('callerId', 'country_code', 
			'caller_number', 'category', 'registered_date', 'registered_by_device')

	def create(self, validated_data):
		"""
		Create and return a caller with validated data
		"""
		if validated_data['caller_number'].startswith('0'):
			validated_data['caller_number'] = validated_data['caller_number'][1:]

		return Caller.objects.create(**validated_data)

	def update(self, instance, validated_data):
		"""
		Update and return existing caller with validated data
		"""
		instance.country_code = validated_data.get('country_code',instance.country_code)
		instance.caller_number = validated_data.get('caller_number', instance.caller_number)
		instance.save()
		return instance







