from django.contrib.auth.models import AbstractUser
from django.db import models

class Brokerage(models.Model):
    STAGE_CHOICES = (
        ('Running', 'Running'),
        ('Lost', 'Lost'),
        ('Prospect', 'Prospect'),
        ('Work In Progress', 'Work In Progress'),
        ('Other', 'Other'),
    )

    city = models.CharField(max_length=500)
    province = models.CharField(max_length=500)
    company_name = models.CharField(max_length=500)
    broker_of_record = models.CharField(max_length=500)
    broker_email = models.CharField(max_length=500)
    deal_administrator_name = models.CharField(max_length=500)
    deal_administrator_email = models.CharField(max_length=500)
    agent_count = models.IntegerField(default=0)
    notes = models.TextField(null=True, blank=True)
    account_manager = models.CharField(max_length=500)
    stage = models.CharField(max_length=500, choices=STAGE_CHOICES, default='Prospect')
    
    def __str__(self):
        return self.company_name


class CustomUser(AbstractUser):
    USER_ROLES = (
        ('Admin', 'Admin'),
        ('Agent', 'Agent'),
        ('Broker', 'Broker'),
        ('Deal Administrator', 'Deal Administrator'),
        ('Other', 'Other'),
    )
    
    role = models.CharField(max_length=100,choices=USER_ROLES,default='Agent')
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    license_number = models.CharField(max_length=100, null=True, blank=True)
    brokerage = models.ForeignKey(Brokerage, on_delete=models.CASCADE, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=100, null=True, blank=True)
    driver_license = models.FileField(upload_to='driver_licenses', null=True, blank=True)
    t4a = models.FileField(upload_to='t4a_licenses', null=True, blank=True)
    void_cheque_or_direct_doposite_form = models.FileField(upload_to='void_cheque_or_direct_doposite_forms', null=True, blank=True)
    annual_commission_statement = models.FileField(upload_to='annual_commission_statements', null=True, blank=True)
    deposit_cheque_or_receipt = models.FileField(upload_to='deposit_cheque_or_receipts', null=True, blank=True)
    institution_id = models.CharField(max_length=100, null=True, blank=True)
    transit_number = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return self.username
