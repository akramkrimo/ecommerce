# Generated by Django 3.0.8 on 2020-09-04 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_auto_20200901_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(related_name='cart', to='store.Product'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Processing', 'processing'), ('Paid', 'paid'), ('Shipping', 'shipping'), ('Closed', 'closed')], default='Processing', max_length=20),
        ),
    ]
