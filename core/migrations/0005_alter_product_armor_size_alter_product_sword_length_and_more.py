# Generated by Django 5.1.2 on 2024-11-19 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_product_uniform_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='armor_size',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='sword_length',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='uniform_size',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]
