from api.models import Caller, Category, CallerCategory
from api.serializers import CallerSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
import logging
from api.utils import APIKeyValidator
import re

###Define logger
callerViewLogger = logging.getLogger(__name__)


class CallerList(APIView):
	permission_classes = (APIKeyValidator,)

	def get(self, request, format=None):
		callers = Caller.objects.all()
		serializer = CallerSerializer(callers, many=True)
		return Response(serializer.data)


	def post(self, request, format=None):
		if isinstance(request.data, list):
			print("I'm in loop create multiple caller")

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
			print("I'm in loop create single caller")
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
		number = item.get('number')
		if number.startswith('0'):
			number = number[1:]
		if number.startswith('+84'):
			number = number[3:]
		if Caller.objects.filter(number=number).exists():
			caller = Caller.objects.filter(number=number)[0]
		else:
			serializer = CallerSerializer(data=item)
			if serializer.is_valid():
				serializer.save()
				caller = Caller.objects.get(pk=serializer.data.get('id'))
		if caller is not None:
			#Save caller_category to intermediate table
			for category in item.get('category'):
				categories = Category.objects.filter(id=category.get('id'))
				check = self.validateCallerCategory(caller, categories[0])
				if isinstance(check, Response):
					continue #### Ignore this item if validate failed
				print("Adding: " + caller.number + " for Category:" + category.get('name'))
				temp_category = Category.objects.get(pk=category['id'])
				caller_category = CallerCategory.objects.create(caller = caller,
                                                                category = temp_category, assign_type = category['assign_type'])

			return True
		callerViewLogger.info("Bad request with invalid data %s", item)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	def validateCaller(self, caller):

		if caller.get('category') is None or len(caller.get('category')) <= 0 or caller.get('category')[0].get('id') is None:
			print("Category Id should be provied")
			return Response('Category Id should be provied', status=status.HTTP_400_BAD_REQUEST)
		if caller.get('id') is not None:
			print("callerId should be null for Post Request")
			return Response('callerId should be null for Post Request', status=status.HTTP_405_METHOD_NOT_ALLOWED)

		if caller.get('number') is None:
			print("Caller Number should be provided ")
			return Response('Caller Number should be provided', status=status.HTTP_400_BAD_REQUEST)

		#check valid phone number
		if re.fullmatch("(0|\+84)?[1-9]{1}[0-9]{8}([0-9]{1})?", caller.get('number')) is None:
			print("Number is not in good format:" + caller.get('number'))
			return Response("Number is not in good format")

		if caller.get('country_code') is None:
			print("Country Code should be provided:" + caller.get('number'))
			return Response('Country Code should be provided', status=status.HTTP_400_BAD_REQUEST)

		if caller.get('registered_by_device') is None:
			print("Registered Device should be provided:" + caller.get('number'))
			return Response('Registered Device should be provided', status=status.HTTP_400_BAD_REQUEST)



	def validateCallerCategory(self, caller, category):
		if Category.objects.filter(id=category.id).exists() is False:
			print("Category Id not found: " + category.id)
			return Response('Category Id not found', status=status.HTTP_404_NOT_FOUND)

		categories = Category.objects.filter(id=category.id)
		if CallerCategory.objects.filter(caller=caller, category=categories[0]).exists():
			print("Number:" + caller.number + " for Category: " + category.name + " exists")
			return Response('Caller Number exists', status=status.HTTP_400_BAD_REQUEST)
		return True
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