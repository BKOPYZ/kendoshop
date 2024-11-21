# Generated by Django 5.1.3 on 2024-11-21 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_shoppingsession_session_delete_cartitem_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='member',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='order',
            name='promotion_code',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='CanceledOrder',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
