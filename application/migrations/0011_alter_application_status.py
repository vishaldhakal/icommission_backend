# Generated by Django 5.0.7 on 2024-10-14 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0010_application_transaction_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Contracted', 'Contracted'), ('Funded', 'Funded'), ('Open', 'Open'), ('Closed', 'Closed'), ('Overdue', 'Overdue')], default='Pending', max_length=20),
        ),
    ]