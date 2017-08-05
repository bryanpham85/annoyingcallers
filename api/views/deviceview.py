from api.models import Device
from api.serializers import DeviceSerializer
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
		#get the deviceId and generate api_request_key then assign back to request for serializer
		if 'id' not in request.data:
			return Response("Device id cannot be empty", status.HTTP_400_BAD_REQUEST)

		api_request_key = CallerAuthUtils.apiRequestKeyGenerator(request.data['id'].encode('utf'))
		request.data['api_request_key'] = api_request_key

		serializer = DeviceSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)