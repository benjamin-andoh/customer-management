# Generated by Django 3.0.7 on 2020-06-29 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_customer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='name',
        ),
    ]