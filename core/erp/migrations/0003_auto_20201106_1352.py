# Generated by Django 3.0.8 on 2020-11-06 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0002_auto_20201106_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.CharField(max_length=50, unique=True, verbose_name='Codigo de Barra'),
        ),
    ]
