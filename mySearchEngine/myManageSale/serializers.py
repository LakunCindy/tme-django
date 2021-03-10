from rest_framework.serializers import ModelSerializer
from myManageSale.models import ProductSale

class ProductSaleSerializer(ModelSerializer):

    class Meta:
        model = ProductSale
        fields = ('id','tigId','discount','sale')
