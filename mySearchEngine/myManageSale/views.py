from django.shortcuts import render
import requests
from rest_framework.views import APIView
from myManageSale.models import ProductSale
from myManageSale.config import baseUrl
from rest_framework.response import Response
from myManageSale.serializers import ProductSaleSerializer
import json
from django.http import Http404


#Mise à jour du sale et du discount d'un produit lorsque l'utilisateur veut qu'il soit en promotion
class UpdateSaleProductDetail(APIView):
    def get(self, request, id, newprice, format=None):
        #si le produit existe déja dans la table, on met à jour le produit avec le nouveau prix (newprice) et le sale = Vrai (True)
        #sinon on créer une nouvelle ligne dans la table avec le discount = nouveau prix (newprice) et le sale = Vrai (True)
        if ProductSale.objects.filter(tigId=id):
            ProductSale.objects.filter(tigId=id).update(discount=newprice, sale=True)
            response = requests.get(baseUrl+'product/'+str(id)+'/')
            product = response.json()
            prod = ProductSale.objects.get(tigId=id)
            serializer = ProductSaleSerializer(prod)
            product['sale'] = serializer.data['sale']
            product['discount'] = serializer.data['discount']
            return Response(product)
        else:
            response = requests.get(baseUrl+'product/'+str(id)+'/')
            product = response.json()
            serializer = ProductSaleSerializer(data={'tigId':str(product['id']),'discount':str(newprice),'sale':str(True)})
            if serializer.is_valid():
                serializer.save()
            product['discount'] = serializer.data['discount']
            product['sale'] = serializer.data['sale']
            return Response(product)

#Mise à jour du sale et du discount d'un produit lorsque l'utilisateur ne veut pas que le produit soit en promotion
class DeleteSaleProductDetail(APIView):
    def remove(self,id):
        ProductSale.objects.filter(tigId=id).update(discount=0.0,sale=False)

    def get_object(self, id):
        try:
            return ProductSale.objects.get(tigId=id)
        except ProductSale.DoesNotExist:
            return Response('id not found',status=404)

    def get(self,request,id,format=None):
        #si le produit existe le discount = 0 et le sale = Faux (false
        prod = self.get_object(id)
        if prod:
            self.remove(id)
            response = requests.get(baseUrl+'product/'+str(id)+'/')
            product = response.json()
            serializer = ProductSaleSerializer(prod)
            product['discount'] = serializer.data['discount']
            product['sale'] = serializer.data['sale']
            return Response(product)
        else:
            return Response('id not found',status=404)
        
