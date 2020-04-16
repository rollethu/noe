# Generated by Django 3.0.5 on 2020-04-16 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_auto_20200408_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='email',
            field=models.EmailField(help_text='Primary communication channel with the patient.', max_length=254),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='end',
            field=models.DateTimeField(blank=True, help_text='The appointment is valid until this time. This probably should be handled more lightly than the start time.', null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='appointments', to='appointments.Location'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='phone_number',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='start',
            field=models.DateTimeField(blank=True, help_text='The appointment is valid from this time.', null=True),
        ),
    ]