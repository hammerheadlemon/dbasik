# Generated by Django 2.0.5 on 2018-06-03 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamap', '0004_auto_20180603_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datamapline',
            name='max_length',
            field=models.IntegerField(blank=True, default=100, null=True),
        ),
    ]
