# Generated by Django 4.0.5 on 2022-06-13 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_tag_order_customer_order_product_product_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='note',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]