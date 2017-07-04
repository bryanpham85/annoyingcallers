from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from api.models import Caller
from api.serializers import CallerSerializer


class UserViewSet(viewsets.ModelViewSet):
	# API endpoint to allow user view and edit
	queryset = User.objects.all().order_by('date_joined')
	serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
	queryset = Group.objects.all().order_by('name')
	serializer_class = GroupSerializer


@csrf_exempt
def caller_list(request):
	"""
	List all caller or create a new caller
	"""
	print("I'm in call list")
	if request.method == "GET":
		callers = Caller.objects.all()
		serializer = CallerSerializer(callers, many=True)
		return JsonResponse(serializer.data, safe=False)
	elif request.method == "POST":
		data = JSONParser().parse(request)
		serializer = CallerSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serialize.data, status=201)
		else:
			return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def caller_detail(request, pk):
	"""
	Retreive update or delete a Caller
	"""
	print("I'm in call detailed")
	try:
		caller = Caller.objects.get(callerId=pk)
	except Caller.DoesNotExist:
		return JsonResponse(status=404)

	if request.method == 'GET':
		serializer = CallerSerializer(caller)
		return JsonResponse(serializer.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = CallerSerializer(caller, data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		else:
			return JsonResponse(serializer.errors, status=404)

	elif request.method == 'DELETE':
		caller.delete()
		return JsonResponse(status=204)



