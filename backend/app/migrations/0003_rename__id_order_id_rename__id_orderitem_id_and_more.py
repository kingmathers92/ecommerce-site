# Generated by Django 4.1.3 on 2022-11-17 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_shippingadress_shippingaddress'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='_id',
            new_name='id',
        ),
    ]
