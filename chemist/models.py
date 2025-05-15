from datetime import date
from django.db import models

class Product(models.Model):
    sku = models.CharField(max_length=100, blank=False, unique=True)
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
    cost_price = models.DecimalField(max_digits=50, decimal_places=2)
    retail_price = models.DecimalField(max_digits=50, decimal_places=2)
    popularity = models.CharField(max_length=100)
    # opening stock
    stock_o = models.PositiveIntegerField()
    # end-of-day inventory
    stock_e = models.PositiveIntegerField()
    sold = models.PositiveIntegerField()
    incoming_stock = models.PositiveIntegerField()
    sugge_number = models.PositiveIntegerField()
    mou = models.PositiveIntegerField()
    arrived_check = models.BooleanField(default=False)

    def __str__(self):
        return f"SKU:{self.sku} _ Product:{self.product_name}"
    

class IncomingOrder(models.Model):
    order_number = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateField(default=date.today)
    expected_arrival = models.DateField(blank=True, null=True)
    arrived_check = models.BooleanField(default=False)
    supplier = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Order_Number:{self.order_number} _ Product:{self.product.product_name} _ Quantity:{self.quantity}"
    

class DailySales(models.Model):
    date = models.DateField(blank=True, null=True)
    sku = models.CharField(max_length=100, blank=False, unique=True)
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
    cost_price = models.DecimalField(max_digits=50, decimal_places=2)
    retail_price = models.DecimalField(max_digits=50, decimal_places=2)
    popularity = models.CharField(max_length=100)
    # opening stock
    stock_o = models.PositiveIntegerField()
    # end-of-day inventory
    stock_e = models.PositiveIntegerField()
    sold = models.PositiveIntegerField()
    incoming_stock = models.PositiveIntegerField()
    mou = models.PositiveIntegerField()
    arrived_check = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date} _ {self.sku} _ {self.product_name}"