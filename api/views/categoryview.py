from api.models import Category
from api.serializers import CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from api.utils import APIKeyValidator

#### Category list view should be used while user assign category to caller
class CategoryList(APIView):
	permission_classes = (APIKeyValidator,)
	
	def get(self, request, format=None):
		categories = Category.objects.all()
		serializer = CategorySerializer(categories, many=True)
		return Response(serializer.data)