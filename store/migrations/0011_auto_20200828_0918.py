# Generated by Django 3.0.8 on 2020-08-28 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20200828_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(related_name='cart', to='store.Product'),
        ),
    ]
