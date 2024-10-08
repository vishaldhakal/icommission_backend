# Generated by Django 5.0.7 on 2024-10-08 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='deal_administrator_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='deal_administrator_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]