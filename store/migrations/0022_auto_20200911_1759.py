# Generated by Django 3.0.8 on 2020-09-11 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_auto_20200911_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(related_name='cart', to='store.Product'),
        ),
    ]
