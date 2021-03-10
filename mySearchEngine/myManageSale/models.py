from django.db import models

# Create your models here.
class ProductSale(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tigId = models.IntegerField(default='-1')
    discount = models.FloatField(default='0.0')
    sale = models.BooleanField(default=False)

    class Meta:
        ordering = ('tigId','discount','sale',)
