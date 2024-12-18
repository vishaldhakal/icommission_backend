# Generated by Django 5.0.7 on 2024-12-14 09:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PortfolioSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exposure_basis', models.DecimalField(decimal_places=2, default=1500000.0, max_digits=15, validators=[django.core.validators.MinValueValidator(0)])),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Portfolio Settings',
            },
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.CharField(max_length=100, unique=True)),
                ('date', models.DateField()),
                ('category', models.CharField(choices=[('SINGLE', 'Single'), ('MULTIPLE', 'Multiple')], default='SINGLE', max_length=20)),
                ('transaction_address', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('PRE_CONSTRUCTION', 'Pre-construction'), ('RESALE', 'Resale'), ('COMMERCIAL', 'Commercial'), ('LINE_OF_CREDIT', 'Line of Credit'), ('ROYALTY_LOAN', 'Royalty Loan'), ('TERM_LOAN', 'Term Loan')], max_length=20)),
                ('purchased_commission_amount', models.DecimalField(decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(0)])),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(0)])),
                ('closing_date', models.DateField()),
                ('agent_commission', models.DecimalField(decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(0)])),
                ('internal_notes', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('OPEN', 'Open'), ('CLOSED', 'Closed')], default='OPEN', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-date'],
                'indexes': [models.Index(fields=['file'], name='deals_deal_file_2be239_idx'), models.Index(fields=['status'], name='deals_deal_status_06cb7b_idx'), models.Index(fields=['type'], name='deals_deal_type_eb1327_idx')],
            },
        ),
    ]
