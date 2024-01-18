from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from api.models import ProductModel
from api.serializers import ProductSerializer


class ProductView(APIView):
    def get(self, request):
        products = ProductModel.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
