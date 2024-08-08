# Generated by Django 5.0.7 on 2024-08-08 11:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommissionAdvanceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateField(auto_now_add=True)),
                ('advance_type', models.CharField(choices=[('Resale Transaction', 'Resale Transaction'), ('Pre-construction', 'Pre-construction'), ('Assignment', 'Assignment'), ('Lease', 'Lease'), ('Other', 'Other')], default='resale', max_length=50)),
                ('transaction_address', models.CharField(max_length=200)),
                ('transaction_closing_date', models.DateField()),
                ('deposit_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('purchase_and_sale_agreement', models.FileField(upload_to='commission_advance_docs')),
                ('waivers_of_conditions', models.FileField(blank=True, null=True, upload_to='commission_advance_docs')),
                ('trade_record_sheet', models.FileField(blank=True, null=True, upload_to='commission_advance_docs')),
                ('deposit_cheque_or_receipt', models.FileField(blank=True, null=True, upload_to='commission_advance_docs')),
                ('copy_of_sold_mls_listing', models.FileField(blank=True, null=True, upload_to='commission_advance_docs')),
                ('amount_requested', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
