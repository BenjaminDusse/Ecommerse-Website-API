# Generated by Django 4.1.2 on 2022-11-13 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0004_alter_product_unit_price"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customer",
            options={
                "ordering": ["user__first_name", "user__last_name"],
                "permissions": [("view_history", "Can view history")],
            },
        ),
    ]
