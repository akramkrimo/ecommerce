# Generated by Django 3.0.8 on 2020-07-31 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='shipping_cost',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]
