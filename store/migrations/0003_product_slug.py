# Generated by Django 4.1.2 on 2022-10-24 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_collection_featured_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=0),
            preserve_default=False,
        ),
    ]
