# Generated by Django 5.1 on 2024-08-11 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_remove_cart_ordered_remove_cart_ordered_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='', max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
