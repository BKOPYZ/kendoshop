# Generated by Django 5.1.2 on 2024-11-25 11:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_promotion_end_date'),
        ('payment', '0006_alter_canceledorder_order_alter_order_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='promotion_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.promotion'),
        ),
    ]
