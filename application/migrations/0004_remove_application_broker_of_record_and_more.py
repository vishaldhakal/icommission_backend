# Generated by Django 5.0.7 on 2024-09-27 05:58

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_application_status_alter_application_upload_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='broker_of_record',
        ),
        migrations.RemoveField(
            model_name='application',
            name='deal_admin_email',
        ),
        migrations.RemoveField(
            model_name='application',
            name='emergency_phone',
        ),
        migrations.RemoveField(
            model_name='application',
            name='mls_listing',
        ),
        migrations.RemoveField(
            model_name='application',
            name='name',
        ),
        migrations.RemoveField(
            model_name='application',
            name='purchase_sale_agreement',
        ),
        migrations.RemoveField(
            model_name='application',
            name='upload_id',
        ),
        migrations.AddField(
            model_name='application',
            name='deal_administrator_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='deal_administrator_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='new_customer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='application',
            name='total_commission_amount_received',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='total_commission_amount_requested',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='transaction_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='transaction_type',
            field=models.CharField(choices=[('Purchase', 'Purchase'), ('Sale', 'Sale'), ('Refinance', 'Refinance')], default='Purchase', max_length=20),
        ),
        migrations.AddField(
            model_name='application',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Contracted', 'Contracted'), ('Funded', 'Funded'), ('Open', 'Open'), ('Closed', 'Closed'), ('Overdue', 'Overdue')], default='Pending', max_length=20),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(choices=[('Valid ID', 'Valid ID'), ('Purchase and Sale Agreement', 'Purchase and Sale Agreement'), ('SOLD MLS Listing', 'SOLD MLS Listing'), ('Annual Commission Statement', 'Annual Commission Statement'), ('T4A', 'T4A'), ('VOID Cheque', 'VOID Cheque'), ('Direct Deposit Form', 'Direct Deposit Form'), ('Waivers of Conditions', 'Waivers of Conditions'), ('Trade Record Sheet', 'Trade Record Sheet'), ('Deposit Cheque/Receipt', 'Deposit Cheque/Receipt'), ('Other', 'Other')], max_length=50)),
                ('file', models.FileField(upload_to='documents/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf'])])),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='application.application')),
            ],
            options={
                'ordering': ['-uploaded_at'],
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note_type', models.CharField(choices=[('Internal', 'Internal'), ('External', 'External')], max_length=10)),
                ('content', models.TextField(default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='application.document')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
