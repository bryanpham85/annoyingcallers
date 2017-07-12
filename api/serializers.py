from django.contrib.auth.models import User, Group
from api.models import Caller, Registered_Device, Category
from rest_framework import serializers

class UserSerializer (serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'username', 'email', 'groups')

class GroupSerializer (serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ('url', 'name')

class CallerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Caller
		fields = ('callerId', 'country_code', 
			'caller_number', 'category', 'registered_date', 'registered_device')

	def create(self, validated_data):
		"""
		Create and return a caller with validated data
		"""
		return Caller.objects.create(**validated_data)

	def update(self, instance, validated_data):
		"""
		Update and return existing caller with validated data
		"""
		instance.country_code = validated_data.get('country_code',instance.country_code)
		instance.caller_number = validated_data.get('caller_number', instance.caller_number)
		instance.save()
		return instance

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ('name', 'category_type', 'created_date')


