# Generated by Django 5.0.7 on 2024-09-13 13:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_remove_document_brokerage_application_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('contracted', 'Contracted'), ('funded', 'Funded'), ('open', 'Open'), ('closed', 'Closed'), ('overdue', 'Overdue')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='application',
            name='upload_id',
            field=models.FileField(help_text='Upload your Valid ID', upload_to='documents/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf'])]),
        ),
    ]
