# Generated by Django 3.0.8 on 2020-08-03 00:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_cart_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='order',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.Order'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(related_name='cart', to='store.Product'),
        ),
    ]
