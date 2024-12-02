# Generated by Django 5.1.3 on 2024-11-21 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_remove_payment_provider_remove_payment_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(default='100/100', max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(default='Parkret', max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='postal_code',
            field=models.CharField(default='11120', max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='province',
            field=models.CharField(default='Nonthaburi', max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='telephone',
            field=models.CharField(default='00000000', max_length=255),
        ),
    ]
