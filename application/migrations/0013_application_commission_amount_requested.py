# Generated by Django 5.0.7 on 2024-10-21 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0012_applicationcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='commission_amount_requested',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
