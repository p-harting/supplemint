# Generated by Django 5.1.1 on 2025-01-03 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0005_order_discount_amount_order_discount_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlineitem',
            name='product_size',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
