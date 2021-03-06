# Generated by Django 3.0.5 on 2020-04-22 14:42

import appointments.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('phone_number', models.CharField(blank=True, max_length=30)),
                ('licence_plate', models.CharField(blank=True, max_length=30)),
                ('normalized_licence_plate', models.CharField(blank=True, max_length=30)),
                ('email', models.EmailField(help_text='Primary communication channel with the patient.', max_length=254)),
                ('gtc', models.CharField(help_text='Accepted version of General Terms and Conditions. Applied to everyone whose Seat belong to this Appointment.', max_length=10)),
                ('privacy_policy', models.CharField(help_text='Accepted version of privacy policy. Applied to everyone whose Seat belong to this Appointment.', max_length=10)),
                ('start', models.DateTimeField(blank=True, help_text='The appointment is valid from this time.', null=True)),
                ('end', models.DateTimeField(blank=True, help_text='The appointment is valid until this time. This probably should be handled more lightly than the start time.', null=True)),
                ('is_registration_completed', models.BooleanField(default=False, help_text='Set before the user is redirected to the "Successful registration" page')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('capacity', models.IntegerField(default=0, help_text='Determines how many Seats can book for this period.')),
                ('usage', models.IntegerField(default=0, help_text="Number of Seats who booked for this period. This should't be edited by humans :)")),
                ('is_active', models.BooleanField(default=True, help_text='Time Slot is only availabe to be booked for if active.')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appointments.Location')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('full_name', models.CharField(max_length=200)),
                ('birth_date', models.DateField()),
                ('healthcare_number', models.CharField(blank=True, max_length=30)),
                ('identity_card_number', models.CharField(max_length=30)),
                ('post_code', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=100)),
                ('address_line1', models.CharField(help_text='Street address', max_length=200)),
                ('address_line2', models.CharField(blank=True, help_text='Apartment, building, floor, suite, door, etc...', max_length=200)),
                ('has_doctor_referral', models.BooleanField(default=False)),
                ('email', models.EmailField(help_text='Notification email for the test results.', max_length=254)),
                ('phone_number', models.CharField(blank=True, max_length=30)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='appointments.Appointment')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='PhoneVerification',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('verified_at', models.DateTimeField(blank=True, null=True)),
                ('code', models.CharField(max_length=255)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phone_verifications', to='appointments.Appointment')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='EmailVerification',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('verified_at', models.DateTimeField(blank=True, null=True)),
                ('code', models.CharField(default=appointments.models._generate_email_code, max_length=255)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_verifications', to='appointments.Appointment')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.AddField(
            model_name='appointment',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='appointments', to='appointments.Location'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='time_slot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appointments.TimeSlot'),
        ),
    ]
