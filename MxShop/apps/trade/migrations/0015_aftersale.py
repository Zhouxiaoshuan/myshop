# Generated by Django 2.1.7 on 2019-07-02 16:59

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trade', '0014_ordergoods_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aftersale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logistics', models.CharField(max_length=200, verbose_name='物流公司')),
                ('number', models.IntegerField(verbose_name='物流单号')),
                ('reason', models.CharField(max_length=200, verbose_name='退换货原因')),
                ('create_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='发起时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '售后',
                'verbose_name_plural': '售后',
            },
        ),
    ]
