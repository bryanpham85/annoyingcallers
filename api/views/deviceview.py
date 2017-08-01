from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.models import Caller, Category, Device
from api.serializers import CallerSerializer, CategorySerializer, DeviceSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from api.utils import CallerAuthUtils

class DeviceDetail(APIView):
	def get_device(self, deviceId):
		try:
			device = Device.objects.get(pk=deviceId)
			return device
		except Device.DoesNotExist:
			raise Http404

	def get(self, request, deviceId, format=None):
		device = self.get_device(deviceId)
		serializer = DeviceSerializer(device)
		return Response(serializer.data)

	def put(self, request, deviceId, format=None):
		device = self.get_device(deviceId)
		serializer = DeviceSerializer(device, request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

	def delete(self, request, deviceId, format=None):
		device = self.get_device(deviceId)
		device.delete()
		return Response(status = status.HTTP_204_NO_CONTENT)

class DeviceList(APIView):
	def post(self, request, format=None):
		print("I'm Here %s", request.data)
		#get the deviceId and generate api_request_key then assign back to request for serializer
		api_request_key = CallerAuthUtils.apiRequestKeyGenerator(request.data['deviceId'].encode('utf'))
		request.data['api_request_key'] = api_request_key
		print("API key after encoded %s", request.data['api_request_key'] )
		serializer = DeviceSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)