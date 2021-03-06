# Generated by Django 3.0.5 on 2020-04-29 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_payment_product_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method_type',
            field=models.CharField(choices=[('SIMPLEPAY', 'SimplePay'), ('ON_SITE', 'Helyszínen')], max_length=255),
        ),
        migrations.AlterField(
            model_name='payment',
            name='product_type',
            field=models.CharField(choices=[('NORMAL_EXAM', 'Normál vizsgálat'), ('PRIORITY_EXAM', 'Elsőbbségi vizsgálat')], max_length=50),
        ),
    ]
