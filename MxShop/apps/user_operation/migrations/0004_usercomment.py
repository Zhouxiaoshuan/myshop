# Generated by Django 2.1.7 on 2019-07-01 15:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_operation', '0003_useraddress_is_default'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.IntegerField(max_length=2, verbose_name='服务')),
                ('quality', models.IntegerField(max_length=2, verbose_name='质量')),
                ('express', models.IntegerField(max_length=2, verbose_name='物流')),
                ('comment', models.CharField(max_length=200, verbose_name='评论')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goods', verbose_name='商品')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '商品评价',
                'verbose_name_plural': '商品评价',
            },
        ),
    ]