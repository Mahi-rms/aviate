# Generated by Django 4.1.1 on 2022-10-01 12:18

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('talent', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hirer',
            fields=[
                ('id', models.UUIDField(db_column='id', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Opportunities',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.CharField(blank=True, max_length=50, null=True)),
                ('opportunity_type', models.CharField(blank=True, choices=[('Internship', 'Internship'), ('Full-Time', 'Full Time'), ('Part-Time', 'Part Time')], max_length=100, null=True)),
                ('compensation', models.JSONField()),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('show_to_talent', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('hirer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hirer_positions', to='hirer.hirer')),
            ],
        ),
        migrations.CreateModel(
            name='HirerDetails',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('company_name', models.CharField(blank=True, max_length=30, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('established_on', models.DateField(blank=True, null=True)),
                ('company_size', models.CharField(blank=True, choices=[('1-50', 'Small'), ('50-500', 'Medium'), ('500-1000', 'Large'), ('1000+', 'Extra Large')], max_length=100, null=True)),
                ('bio', models.CharField(blank=True, max_length=200, null=True)),
                ('profile_photo_url', models.CharField(blank=True, max_length=200, null=True)),
                ('linkedin_url', models.CharField(blank=True, max_length=100, null=True)),
                ('facebook_url', models.CharField(blank=True, max_length=100, null=True)),
                ('instagram_url', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('hirer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hirer', to='hirer.hirer')),
            ],
        ),
        migrations.CreateModel(
            name='Candidature',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('resume_url', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.CharField(blank=True, choices=[('Applied', 'Applied'), ('Shortlisted', 'Shortlisted'), ('Selected', 'Selected'), ('Not Considered at this time', 'Not Considered'), ('Withdrawn', 'Withdrawn')], default='Applied', max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('opportunity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='opportunity', to='hirer.opportunities')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='candidate', to='talent.user')),
            ],
        ),
    ]
