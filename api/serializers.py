from django.contrib.auth.models import User, Group
from api.models import Caller, Registered_Device, Category, Caller_Categories
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
	# callerId = serializers.IntegerField(read_only=True)
	# country_code = serializers.CharField(required=True, allow_blank=False)
	# caller_number = serializers.CharField(required=True, allow_blank=False, max_length=11)
	# registered_date = serializers.DateTimeField(required=False)
	# registered_by = serializers.CharField(required=True)
	class Meta:
		model = Caller
		fields = ('callerId', 'country_code', 
			'caller_number', 'registered_date', 'registered_by')

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


