from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.models import Caller, Category
from api.serializers import CallerSerializer, CategorySerializer
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
		serializer = CallerSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
		serializer = CallerSerializer(caller, request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		caller = self.get_object(pk)
		caller.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryList(APIView):
	def get(self, request, format=None):
		categories = Category.objects.all()
		serializer = CategorySerializer(categories, many=True)
		return Response(serializer.data)
