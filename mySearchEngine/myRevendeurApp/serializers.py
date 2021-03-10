from rest_framework.serializers import ModelSerializer
from myRevendeurApp.models import QuantityInStock

class QuantityInStockSerializer(ModelSerializer):

    def get(self,obj):
        return obj.quantityInStock.quantity

    class Meta:
        model = QuantityInStock
        fields = ('id','tigId','quantity')
