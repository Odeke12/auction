# Generated by Django 3.0.8 on 2020-08-21 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20200820_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='final_buyer',
            field=models.CharField(blank=True, max_length=23),
        ),
    ]
