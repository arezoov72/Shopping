# Generated by Django 3.2.9 on 2022-04-23 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_rename_price_product_unit_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='custumer',
            new_name='customer',
        ),
    ]
