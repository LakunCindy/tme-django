from django.db import models

# Create your models here.
class QuantityInStock(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tigId = models.IntegerField(default='-1')
    quantity = models.IntegerField(default='0')

    class Meta:
        ordering = ('tigId','quantity',)