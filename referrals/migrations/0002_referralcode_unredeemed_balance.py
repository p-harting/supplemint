# Generated by Django 5.1.1 on 2024-12-31 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referrals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='referralcode',
            name='unredeemed_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]