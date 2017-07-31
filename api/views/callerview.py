from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.models import Caller, Category, Device, Caller_Category
from api.serializers import CallerSerializer, CategorySerializer, DeviceSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
import logging

###Define logger
callerViewLogger = logging.getLogger(__name__)


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

			#Save caller_category to intermediate table
			for category in item.get('category'):
				temp_category = Category.objects.get(pk=category['category_id'])
				caller_category = Caller_Category.objects.create(caller_id = caller, 
					category_id = temp_category, assign_type = category['assign_type'])
			serializer = CallerSerializer(caller)
			return serializer
		callerViewLogger.info("Bad request with invalid data %s", item)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	def validateCaller(self, caller):
		return True
		# if caller.get('category') is None or len(caller.get('category')) <= 0 or caller.get('category')[0].get('id') is None:
		# 	return Response('Category Id should be provied', status=status.HTTP_400_BAD_REQUEST)
		# if Category.objects.filter(id=caller.get('category')[0].get('id')).exists() is False:
		# 	return Response('Category Id not found', status=status.HTTP_404_NOT_FOUND)

		# if caller.get('callerId') is not None:
		# 	return Response('callerId should be null for Post Request', status=status.HTTP_405_METHOD_NOT_ALLOWED)

		# if caller.get('caller_number') is None:
		# 	return Response('Caller Number should be provied', status=status.HTTP_400_BAD_REQUEST)

		# if caller.get('country_code') is None:
		# 	return Response('Country Code should be provied', status=status.HTTP_400_BAD_REQUEST)

		# if caller.get('registered_by_device') is None:
		# 	return Response('Registered Device should be provied', status=status.HTTP_400_BAD_REQUEST)

		# if Caller.objects.filter(caller_number=caller.get('caller_number')).exists():
		# 	callers = Caller.objects.filter(caller_number=caller.get('caller_number'))
		# 	for index in range(len(callers)):
		# 		exist = callers[index]
		# 		if exist.category.filter(id=caller.get('category')[0].get('id')).exists():
		# 			return Response('Caller Number exists', status=status.HTTP_400_BAD_REQUEST)
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