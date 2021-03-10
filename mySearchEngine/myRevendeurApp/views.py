import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from myRevendeurApp.config import baseUrl
from myRevendeurApp.models import QuantityInStock
from myManageSale.models import ProductSale
from myManageSale.serializers import ProductSaleSerializer
from myRevendeurApp.serializers import QuantityInStockSerializer
from django.http import Http404
import json


class UpdateSale():
    # Mise à jour de la du sale et du discount du produit en fonction de l'id
    def update(self,prod,response,id):
        #En fonction de la condition on met à jour la valeur du sale et du discount depuis la table myManageSale.productsale
        #retourne le produit json avec les valeurs discount et sale de la bdd  
        if prod.quantity < 16:
            ProductSale.objects.filter(tigId=id).update(sale=False,discount=0.0)
            new_prod_in_manage_sale = ProductSale.objects.get(tigId=id)
            serializer = ProductSaleSerializer(new_prod_in_manage_sale)
            response['sale'] = serializer.data['sale']
            response['discount'] = serializer.data['discount']
            return response
        elif 16 <= prod.quantity <= 64:
            new_price = round(response['price'] * 0.8,2)
            ProductSale.objects.filter(tigId=id).update(sale=True,discount=new_price)
            new_prod_in_manage_sale = ProductSale.objects.get(tigId=id)
            serializer = ProductSaleSerializer(new_prod_in_manage_sale)
            response['sale'] = serializer.data['sale']
            response['discount'] = serializer.data['discount']
            return response
        else:
            new_price = round(response['price'] * 0.5,2)
            ProductSale.objects.filter(tigId=id).update(sale=True,discount=new_price)
            new_prod_in_manage_sale = ProductSale.objects.get(tigId=id)
            serializer = ProductSaleSerializer(new_prod_in_manage_sale)
            response['sale'] = serializer.data['sale']
            response['discount'] = serializer.data['discount']
            return response


class InfoStockProducts(APIView):
     def get(self, request, format=None):
        res=[]
        for prod in QuantityInStock.objects.all():
            serializer = QuantityInStockSerializer(prod)
            response = requests.get(baseUrl+'product/'+str(serializer.data['tigId'])+'/')
            jsondata = response.json()
            res.append(jsondata)
        return Response(res)

class InfoStockProductDetail(APIView):
    def get_object(self, pk):
        try:
            return QuantityInStock.objects.get(pk=pk)
        except QuantityInStock.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        prod = self.get_object(pk)
        serializer = QuantityInStockSerializer(prod)
        response = json.loads(requests.get(baseUrl+'product/'+str(pk)+'/').text)
        response['quantity'] = serializer.data['quantity']
        return Response(response)

#Incrémente la quantité du produit et met à jour le sale et le discount en fonction du produit
class IncrementStock(APIView):
    #calcul de la nouvelle quantité et update dans la table du produit
    def increment_quantity(self, id, number):
        prod = QuantityInStock.objects.get(tigId=id)
        old_quantity = prod.quantity
        new_quantity = old_quantity + number
        QuantityInStock.objects.filter(tigId=id).update(quantity = new_quantity)
    
    def get_object(self, id):
        try:
            return QuantityInStock.objects.get(tigId=id)
        except QuantityInStock.DoesNotExist:
            print('not exist')
            raise Http404

    def get(self,request,id,number,format=None):
        prod = self.get_object(id)
        if prod:
            response = requests.get(baseUrl+'product/'+str(id)+'/')
            json_response = response.json()
            self.increment_quantity(id,number)
            #récupère le produit de la table myRevendeurApp_quantityInStock avec la quantité à jour pour
            #update le sale et le discount du produit
            new_prod = self.get_object(id)
            response_after_update_sale = UpdateSale.update(self,new_prod,json_response,id)
            serializer = QuantityInStockSerializer(new_prod)
            response_after_update_sale['quantity'] = serializer.data['quantity']
            return Response(response_after_update_sale)
        else:
            return Response('id not found',status=404)

##Incrémente la quantité du produit et met à jour le sale et le discount en fonction du produit
class DecrementStock(APIView):
    #récupération de la nouvelle quantité e
    def new_quantity(self, id, number):
        prod = QuantityInStock.objects.get(tigId=id)
        old_quantity = prod.quantity
        new_quantity = old_quantity - number
        return new_quantity

    def get_object(self, id):
        try:
            return QuantityInStock.objects.get(tigId=id)
        except QuantityInStock.DoesNotExist:
            return Response('id not found',status=404)
    
    def get(self,request,id,number,format=None):
        prod_in_quantity_in_stock = self.get_object(id)
        if prod_in_quantity_in_stock:
            new_quantity = self.new_quantity(id,number)
            if new_quantity >= 0:
                response = requests.get(baseUrl+'product/'+str(id)+'/')
                prod_in_database = response.json()
                QuantityInStock.objects.filter(tigId=id).update(quantity = new_quantity)
                #récupère le produit de la table myRevendeurApp_quantityInStock avec la quantité à jour pour
                #update le sale et le discount du produit
                new_prod = self.get_object(id)
                new_response = UpdateSale.update(self,new_prod,prod_in_database,id)
                serializer = QuantityInStockSerializer(new_prod)
                new_response['quantity'] = serializer.data['quantity']
                return Response(new_response)
            else:
                return Response('cannot decrement, plese verify quantity',status=405)
        else:
            return Response('id not found',status=404)


        
        
