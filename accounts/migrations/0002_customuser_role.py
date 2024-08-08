# Generated by Django 5.0.7 on 2024-08-08 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Broker', 'Broker'), ('Deal Administrator', 'Deal Administrator'), ('Other', 'Other')], default='Broker', max_length=100),
        ),
    ]
