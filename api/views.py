from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.models import Caller, Category, Registered_Device
from api.serializers import CallerSerializer, CategorySerializer, Registered_DeviceSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response


class CallerList(APIView):

	def get(self, request, format=None):
		callers = Caller.objects.all()
		serializer = CallerSerializer(callers, many=True)
		return Response(serializer.data)


	def post(self, request, format=None):
		if isinstance(request.data, list):

			for index in range(len(request.data)):
				item = request.data[index]
				check = self.validateCaller(item)
				if isinstance(check, Response):
					continue #### Ignore this item if validate failed

				ret = self.saveItem(item)
				if isinstance(ret, Response):
					continue
			callers = Caller.objects.all()
			serializer = CallerSerializer(callers, many=True)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			check = self.validateCaller(request.data)
			if isinstance(check, Response):
				return check
			ret = self.saveItem(request.data)
			if isinstance(ret, Response):
				return ret
			callers = Caller.objects.all()
			serializer = CallerSerializer(callers, many=True)
			return Response(serializer.data, status=status.HTTP_201_CREATED)

	def saveItem(self, item):
		serializer = CallerSerializer(data=item)
		if serializer.is_valid():
			serializer.save()
			caller = Caller.objects.get(pk=serializer.data.get('callerId'))
			category = Category.objects.get(pk=item.get('category')[0]['id'])
			caller.category.add(category)
			serializer = CallerSerializer(caller)
			return serializer
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	def validateCaller(self, caller):
		if caller.get('category') is None or len(caller.get('category')) <= 0 or caller.get('category')[0].get('id') is None:
			return Response('Category Id should be provied', status=status.HTTP_400_BAD_REQUEST)
		if Category.objects.filter(id=caller.get('category')[0].get('id')).exists() is False:
			return Response('Category Id not found', status=status.HTTP_404_NOT_FOUND)

		if caller.get('callerId') is not None:
			return Response('callerId should be null for Post Request', status=status.HTTP_405_METHOD_NOT_ALLOWED)

		if caller.get('caller_number') is None:
			return Response('Caller Number should be provied', status=status.HTTP_400_BAD_REQUEST)

		if caller.get('country_code') is None:
			return Response('Country Code should be provied', status=status.HTTP_400_BAD_REQUEST)

		if caller.get('registered_device') is None:
			return Response('Registered Device should be provied', status=status.HTTP_400_BAD_REQUEST)

		if Caller.objects.filter(caller_number=caller.get('caller_number')).exists():
			callers = Caller.objects.filter(caller_number=caller.get('caller_number'))
			for index in range(len(callers)):
				exist = callers[index]
				if exist.category.filter(id=caller.get('category')[0].get('id')).exists():
					return Response('Caller Number exists', status=status.HTTP_400_BAD_REQUEST)


class CallerDetail(APIView):

	def get_object(self, pk):
		try:
			caller = Caller.objects.get(pk=pk)
			return caller
		except Caller.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		caller = self.get_object(pk)
		serializer = CallerSerializer(caller)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		caller = self.get_object(pk)
		Category.objects.get(1)
		serializer = CallerSerializer(caller, request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		caller = self.get_object(pk)
		caller.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

#### Category list view should be used while user assign category to caller
class CategoryList(APIView):
	def get(self, request, format=None):
		categories = Category.objects.all()
		serializer = CategorySerializer(categories, many=True)
		return Response(serializer.data)


#### Registered device need to get details only

class Registered_DeviceDetail(APIView):
	def get_device(self, deviceId):
		try:
			device = Registered_Device.objects.get(pk=deviceId)
			return device
		except Registered_Device.DoesNotExist:
			raise Http404

	def get(self, request, deviceId, format=None):
		device = self.get_device(deviceId)
		serializer = Registered_DeviceSerializer(device)
		return Response(serializer.data)

	def put(self, request, deviceId, format=None):
		device = self.get_device(deviceId)
		serializer = Registered_DeviceSerializer(device, request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

	def delete(self, request, deviceId, format=None):
		device = self.get_device(deviceId)
		device.delete()
		return Response(status = status.HTTP_204_NO_CONTENT)

class Registered_DeviceList(APIView):
	def post(self, request, format=None):
		serializer = Registered_DeviceSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

