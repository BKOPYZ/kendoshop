# Generated by Django 5.1.2 on 2024-11-20 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_product_armor_size_alter_product_sword_length_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingsession',
            name='session',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
        migrations.DeleteModel(
            name='ShoppingSession',
        ),
    ]
