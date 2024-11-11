# Generated by Django 5.0.7 on 2024-10-21 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_customuser_driver_license'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='annual_commission_statement',
            field=models.FileField(blank=True, null=True, upload_to='annual_commission_statements'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='deposit_cheque_or_receipt',
            field=models.FileField(blank=True, null=True, upload_to='deposit_cheque_or_receipts'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='t4a',
            field=models.FileField(blank=True, null=True, upload_to='t4a_licenses'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='void_cheque_or_direct_doposite_form',
            field=models.FileField(blank=True, null=True, upload_to='void_cheque_or_direct_doposite_forms'),
        ),
    ]