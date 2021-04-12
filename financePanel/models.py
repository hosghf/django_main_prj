from django.db import models

# Create your models here.

class stockPrice(models.Model):
    name = models.CharField(max_length=30, help_text="hellooo")
    symbol = models.CharField(max_length=30, default=12)
    market = models.CharField(null=True, blank=True,max_length=30)
    stok_type = models.CharField(null=True, blank=True,max_length=1)
    size = models.DecimalField(max_digits=16, decimal_places=5)
    open = models.DecimalField(null=True, blank=True, max_digits=16, decimal_places=5)
    date = models.DateTimeField(null=True, blank=True)
    low = models.DecimalField(null=True, blank=True,max_digits=16, decimal_places=5)
    high = models.DecimalField(null=True, blank=True,max_digits=16, decimal_places=5)
    close_price = models.DecimalField(null=True, blank=True,max_digits=16, decimal_places=5)
    volume = models.DecimalField(null=True, blank=True,max_digits=16, decimal_places=5)