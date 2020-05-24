# Generated by Django 3.0.6 on 2020-05-24 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_auto_20200524_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='availability',
            field=models.CharField(choices=[('av', 'Available'), ('bo', 'Booked'), ('so', 'Sold')], max_length=2, null=True),
        ),
    ]