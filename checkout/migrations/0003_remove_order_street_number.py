# Generated by Django 4.2.17 on 2025-04-10 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_alter_order_country_alter_order_user_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='street_number',
        ),
    ]
