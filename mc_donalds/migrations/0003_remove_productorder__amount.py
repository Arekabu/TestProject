# Generated by Django 5.1.6 on 2025-04-01 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mc_donalds', '0002_remove_productorder_amount_productorder__amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productorder',
            name='_amount',
        ),
    ]
