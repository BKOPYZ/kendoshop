# Generated by Django 5.1.3 on 2024-11-23 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0014_remove_userpayment_unique_user_payment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='telephone',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='telephone',
            field=models.CharField(max_length=10),
        ),
    ]
