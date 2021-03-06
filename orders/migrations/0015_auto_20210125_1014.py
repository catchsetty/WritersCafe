# Generated by Django 2.2.13 on 2021-01-25 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_auto_20210125_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashrecord',
            name='CurrentBalance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='cashrecord',
            name='OpeningBalance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='cashrecorddetail',
            name='Amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='itemTotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='unitPrice',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='unitPrice_before_tax',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='unitPrice_tax',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
    ]
