# Generated by Django 4.1.5 on 2023-07-13 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='category_status',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='sub_category_status',
        ),
    ]
