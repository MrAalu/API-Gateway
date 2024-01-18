from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from api.models import OrderModel
from api.serializers import OrderSerializer


class OrderView(APIView):
    def get(self, request):
        orders = OrderModel.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
