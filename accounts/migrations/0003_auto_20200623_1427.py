# Generated by Django 3.0.7 on 2020-06-23 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_order_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, to='accounts.Customer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, to='accounts.Product'),
            preserve_default=False,
        ),
    ]
