# Generated by Django 5.0.2 on 2024-03-14 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('karma', '0002_alter_product_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='price',
            field=models.IntegerField(default=1),
        ),
    ]
