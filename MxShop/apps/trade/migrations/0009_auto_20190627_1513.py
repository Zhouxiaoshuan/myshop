# Generated by Django 2.1.7 on 2019-06-27 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0008_auto_20190627_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergoods',
            name='order',
            field=models.IntegerField(verbose_name='订单信息'),
        ),
    ]
