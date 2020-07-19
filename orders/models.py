from django.db import models
from enum import Enum
import datetime


# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    brand = models.CharField(max_length=100, blank=True)

    PER_MEASUREMENT = (
        ('e', ''),
        ('Bottle', 'Bottle'),
        ('KG', 'KG'),
        ('Nos', 'NOs'),
        ('Tin', 'Tin'),
        ('Packet', 'Packet'),
        ('Jar', 'Jar'),
        ('Litre', 'Litre'),
        ('Box', 'Box')
    )

    GST_RATE =(
        (0, '0'),
        (5, '5'),
        (12, '12'),
        (18, '18')
    )
    GSTRate = models.IntegerField(choices=GST_RATE, default=2)
    per = models.CharField(max_length=10, choices= PER_MEASUREMENT, default='e', help_text='Measurement. Per box/tin/kg')

    def __str__(self):
        return self.name


class Suppliers(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True)
    GSTIN = models.CharField(max_length=20, blank=True)
    contact = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class StatusChoice(Enum):
    OD = "Ordered"
    RD = "Received"
    RT = "Returned"


class Status(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=10)

    def __str__(self):
        return self.status


class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    supplier_id = models.ForeignKey(Suppliers, on_delete=models.SET_NULL, null=True)
    ordered_date = models.DateField()
    order_status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    ordered_by = models.CharField(max_length=80)
    order_total_before_tax = models.FloatField(default=0)
    order_total_after_tax = models.FloatField(default=0)
    gst_tax = models.FloatField(default=0)

    class Meta:
        ordering = ['order_status']
        verbose_name = 'Order'

    def __str__(self):
        return f'{self.id}, ({self.order_status})'


class OrderDetails(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Orders, on_delete=models.SET_NULL, null=True)
    ingredient_id = models.ForeignKey(Ingredients, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    transaction_date = models.DateField(default=datetime.date.today)
    unitPrice = models.FloatField(default=0)
    quantity = models.IntegerField(default=0, null=True)
    unitPrice_before_tax = models.FloatField(default=0)
    unitPrice_tax = models.FloatField(default=0)
    itemTotal = models.FloatField(default=0)

    def __str__(self):
        return f'{self.id} ({self.ingredient_id.name}) ({self.ingredient_id.per})'

    def get_measurement(self):
        return self.ingredient_id.per

    def get_item_value(self):
        item_price = self.unitPrice * self.quantity
        self.unitPrice_before_tax= item_price
        return item_price

    def get_tax_value(self):
        tax_price = self.get_item_value() * self.ingredient_id.GSTRate / 100
        self.unitPrice_tax = tax_price
        return tax_price

    def save(self, *args, **kwargs):
        self.itemTotal = self.get_item_value() + self.get_tax_value()
        self.transaction_date = self.order_id.ordered_date
        super(OrderDetails, self).save(*args, **kwargs)


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    ingredient_id = models.ForeignKey(Ingredients, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.id}, {self.ingredient_id}'


class CashRecord(models.Model):
    TransactDate = models.DateField(unique=True, default=datetime.date.today)
    OpeningBalance = models.FloatField(default=0)
    CurrentBalance = models.FloatField(default=0)

    def __str__(self):
        return f'{self.TransactDate}'


class CashRecordDetail(models.Model):
    cashRecordId = models.ForeignKey(CashRecord, on_delete=models.SET_NULL, null=True)
    category = models.CharField(default='Miscellaneous', max_length=50)
    sub_category = models.CharField(default='sub-type', unique=True, max_length=50)

    Cash_option = (
        ('Debit', 'Debit'),
        ('Credit', 'Credit')
    )
    Type = models.CharField(choices=Cash_option, default='Debit', max_length= 6)
    Amount = models.FloatField(default=0)

    def __str__(self):
        return f'{self.cashRecordId}'
