# Generated by Django 4.0.6 on 2022-07-22 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_addon_alter_pickup_options_alter_pickup_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcel',
            name='addons',
            field=models.ManyToManyField(to='main_app.addon'),
        ),
    ]
