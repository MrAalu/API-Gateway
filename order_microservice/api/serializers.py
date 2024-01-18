from rest_framework.serializers import ModelSerializer
from api.models import OrderModel


class OrderSerializer(ModelSerializer):
    class Meta:
        model = OrderModel
        fields = "__all__"
