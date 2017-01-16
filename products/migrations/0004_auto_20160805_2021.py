# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_productimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to=products.models.image_upload_to),
        ),
        migrations.AddField(
            model_name='products',
            name='categories',
            field=models.ManyToManyField(to='products.category', blank=True),
        ),
        migrations.AddField(
            model_name='products',
            name='default',
            field=models.ForeignKey(to='products.category', related_name='default_category', null=True, blank=True),
        ),
    ]
