# Generated by Django 2.2.13 on 2020-08-12 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20200812_1636'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockdetails',
            old_name='stock_date',
            new_name='stock_id',
        ),
    ]