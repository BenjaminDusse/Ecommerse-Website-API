# Generated by Django 3.2.4 on 2023-02-20 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_productimage_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='caption',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
