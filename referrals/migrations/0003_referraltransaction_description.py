# Generated by Django 5.1.1 on 2024-12-31 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referrals', '0002_referralcode_unredeemed_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='referraltransaction',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
