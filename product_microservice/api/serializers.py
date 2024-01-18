from rest_framework.serializers import ModelSerializer
from api.models import ProductModel


class ProductSerializer(ModelSerializer):
    class Meta:
        model = ProductModel
        fields = "__all__"
