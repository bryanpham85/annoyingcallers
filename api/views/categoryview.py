from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.models import Caller, Category, Device
from api.serializers import CallerSerializer, CategorySerializer, DeviceSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response

#### Category list view should be used while user assign category to caller
class CategoryList(APIView):
	def get(self, request, format=None):
		categories = Category.objects.all()
		serializer = CategorySerializer(categories, many=True)
		return Response(serializer.data)