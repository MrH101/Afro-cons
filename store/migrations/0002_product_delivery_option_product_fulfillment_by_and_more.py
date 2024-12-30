# Generated by Django 4.2.5 on 2024-11-11 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='delivery_option',
            field=models.CharField(choices=[('selected_countries', 'Selected Countries'), ('worldwide', 'Worldwide Delivery'), ('local', 'Local Delivery')], default='worldwide', max_length=20),
        ),
        migrations.AddField(
            model_name='product',
            name='fulfillment_by',
            field=models.CharField(choices=[('seller', 'Fulfilled by Seller'), ('company', 'Fulfilled by Company')], default='seller', max_length=10),
        ),
        migrations.AddField(
            model_name='product',
            name='variants',
            field=models.JSONField(blank=True, default=dict, help_text='Store variants like color, size, etc. as a JSON object'),
        ),
    ]
