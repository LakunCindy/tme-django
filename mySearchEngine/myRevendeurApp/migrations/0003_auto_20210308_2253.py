# Generated by Django 3.1.7 on 2021-03-08 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myRevendeurApp', '0002_auto_20210308_2122'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quantityinstock',
            options={'ordering': ('tigId', 'quantity')},
        ),
        migrations.RenameField(
            model_name='quantityinstock',
            old_name='quantityInStock',
            new_name='quantity',
        ),
    ]
