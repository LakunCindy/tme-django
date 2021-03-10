from django.core.management.base import BaseCommand, CommandError
from myRevendeurApp.models import QuantityInStock
from myRevendeurApp.serializers import QuantityInStockSerializer
from myRevendeurApp.config import baseUrl
import requests
import time

class Command(BaseCommand):
    help = 'Refresh the list of products which are on sale.'

    def handle(self, *args, **options):
        self.stdout.write('['+time.ctime()+'] Refreshing data...')
        response = requests.get(baseUrl+'products/')
        jsondata = response.json()
        QuantityInStock.objects.all().delete()
        for product in jsondata:
                # serializer = QuantityInStockSerializer(data={'quantityInStock':str('0')})
                serializer_tigId = QuantityInStockSerializer(data={'tigId':str(product['id'])})
                if serializer_tigId.is_valid():
                    # serializer.save()
                    serializer_tigId.save()
                    self.stdout.write(self.style.SUCCESS('['+time.ctime()+'] Successfully added product id="%s"' % product['id']))
        self.stdout.write('['+time.ctime()+'] Data refresh terminated.')
