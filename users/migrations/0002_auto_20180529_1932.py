# Generated by Django 2.0.4 on 2018-05-29 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='organisation',
            field=models.ManyToManyField(to='users.Organisation'),
        ),
    ]