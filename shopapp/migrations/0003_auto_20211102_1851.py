# Generated by Django 3.2.7 on 2021-11-02 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0002_auto_20211101_1015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='availability',
        ),
        migrations.AddField(
            model_name='product',
            name='Quantity',
            field=models.IntegerField(default=0, max_length=128),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
