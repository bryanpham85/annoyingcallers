from rest_framework import permissions
from api.models import Device

class APIKeyValidator(permissions.BasePermission):
    
    def has_permission(selfself, request, view):
        #the app_request_key send through header, should get through dictionary to avoid not such key send
        #check if key existing in device table
        key = request.META.get('HTTP_API_REQUEST_KEY', None);
        if key is not None:
            deviceExisted = Device.objects.filter(api_request_key=key).exists()
            return deviceExisted
        else:
            return False
        