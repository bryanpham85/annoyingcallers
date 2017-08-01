from api.models import Device
from hashlib import blake2b
from hmac import digest_size

class CallerAuthUtils:
    
    @staticmethod
    def apiRequestKeyGenerator(deviceId):
        h = blake2b(digest_size=22)
        h.update(deviceId)
        hashed_value = h.hexdigest()
        return hashed_value
    
    @staticmethod
    def authenticateApiCallWithDeviceKey(deviceId, key):
        device = Device.objects.get(pk=deviceId)
        return device.app_request_key == key
    
    class Meta:
        app_lable = 'api'