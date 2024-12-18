# Generated by Django 5.0.7 on 2024-12-14 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0002_alter_deal_options_alter_deal_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='category',
            field=models.CharField(choices=[('Single', 'Single'), ('Multiple', 'Multiple')], db_index=True, default='Single', max_length=255),
        ),
        migrations.AlterField(
            model_name='deal',
            name='company',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='deal',
            name='file',
            field=models.CharField(db_index=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='deal',
            name='name',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='deal',
            name='status',
            field=models.CharField(choices=[('Open', 'Open'), ('Closed', 'Closed')], db_index=True, default='Open', max_length=255),
        ),
        migrations.AlterField(
            model_name='deal',
            name='type',
            field=models.CharField(choices=[('Pre-construction', 'Pre-construction'), ('Resale', 'Resale'), ('Commercial', 'Commercial'), ('Line of Credit', 'Line of Credit'), ('Royalty Loan', 'Royalty Loan'), ('Term Loan', 'Term Loan'), ('Bridge Loan (Private)', 'Bridge Loan (Private)')], db_index=True, max_length=255),
        ),
    ]
