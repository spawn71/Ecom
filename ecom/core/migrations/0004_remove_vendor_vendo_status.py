# Generated by Django 4.1.5 on 2023-07-13 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_product_tags_product_vendor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='vendo_status',
        ),
    ]
