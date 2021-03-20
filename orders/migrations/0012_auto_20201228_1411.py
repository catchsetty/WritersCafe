# Generated by Django 2.2.13 on 2020-12-28 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20201228_1406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdetails',
            name='status',
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_status',
            field=models.CharField(choices=[('New', 'New'), ('Received', 'Received')], default='Received', max_length=20),
        ),
        migrations.DeleteModel(
            name='Status',
        ),
    ]