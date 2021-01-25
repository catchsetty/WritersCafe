from django.db import models
import datetime


# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Categories'

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
        return f'{self.name}'


class Suppliers(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True)
    GSTIN = models.CharField(max_length=20, blank=True)
    contact = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class StockInstance(models.Model):
    id = models.AutoField(primary_key=True)
    stock_date = models.DateField(default=datetime.date.today, unique=True)
    STOCK_STATUS = (
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done')
    )

    stock_status = models.CharField(choices=STOCK_STATUS, default='New', max_length=10)

    def __str__(self):
        return f'{self.stock_date}, {self.stock_status}'


class StockDetails(models.Model):
    stock_id = models.ForeignKey(StockInstance, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredients, on_delete= models.CASCADE)
    quantity = models.IntegerField(default=0, null=True)

    def __str__(self):
        return f'{self.ingredient_id}, {self.quantity}'


class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    supplier_id = models.ForeignKey(Suppliers, on_delete=models.SET_NULL, null=True)
    ordered_date = models.DateField(default=datetime.date.today)
    ORDER_STATUS = (
        ('New', 'New'),
        ('Received', 'Received'),
        ('Paid', 'Paid')
    )
    PAYMENT_STATUS = (
        ('Fully-Paid', 'Fully-Paid'),
        ('Partial', 'Partial'),
        ('Not-Paid', 'Not-Paid')
    )
    order_status = models.CharField(choices=ORDER_STATUS, max_length=20, default='Received')
    ordered_by = models.CharField(max_length=80, blank=True, default='WC')
    pay_status = models.CharField(choices=PAYMENT_STATUS, max_length=20, default='Not-Paid')

    class Meta:
        ordering = ['ordered_date']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'{self.id}'


class OrderDetails(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Orders, on_delete=models.PROTECT, null=True)
    ingredient_id = models.ForeignKey(Ingredients, on_delete=models.SET_NULL, null=True)
    transaction_date = models.DateField(default=datetime.date.today)
    unitPrice = models.DecimalField(default=0, max_digits=9, decimal_places=2)
    quantity = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    unitPrice_before_tax = models.DecimalField(default=0, max_digits=9, decimal_places=2)
    unitPrice_tax = models.DecimalField(default=0, max_digits=9, decimal_places=2)
    itemTotal = models.DecimalField(default=0, max_digits=9, decimal_places=2)

    class Meta:
        verbose_name = 'Order Details'
        verbose_name_plural = 'Order Details'

    def __str__(self):
        return f'{self.id}'

    def get_measurement(self):
        return self.ingredient_id.per

    def get_item_value(self):
        item_total = self.unitPrice * self.quantity
        self.itemTotal = item_total
        return item_total

    def get_tax_value(self):
        tax_price = self.get_item_value() * self.ingredient_id.GSTRate / 100
        self.unitPrice_tax = tax_price
        return tax_price

    def save(self, *args, **kwargs):
        self.unitPrice_before_tax = self.get_item_value() - self.get_tax_value()
        super(OrderDetails, self).save(*args, **kwargs)


class CashRecord(models.Model):
    TransactDate = models.DateField(unique=True, default=datetime.date.today)
    OpeningBalance = models.DecimalField(default=0, max_digits=9, decimal_places=2)
    CurrentBalance = models.DecimalField(default=0, max_digits=9, decimal_places=2)

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
    Amount = models.DecimalField(default=0, max_digits=9, decimal_places=2)

    def __str__(self):
        return f'{self.cashRecordId}'
