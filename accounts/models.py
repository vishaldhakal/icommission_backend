from django.contrib.auth.models import AbstractUser
from django.db import models

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
    current_brokerage_name = models.CharField(max_length=100, null=True, blank=True)
    brokerage_phone = models.CharField(max_length=100, null=True, blank=True)
    broker_of_record_name = models.CharField(max_length=100, null=True, blank=True)
    broker_of_record_email = models.CharField(max_length=100, null=True, blank=True)
    deal_administrator_name = models.CharField(max_length=100, null=True, blank=True)
    deal_administrator_email = models.EmailField(null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=100, null=True, blank=True)
    driver_license = models.FileField(upload_to='driver_licenses', null=True, blank=True)
    t4a = models.FileField(upload_to='t4a_licenses', null=True, blank=True)
    void_cheque_or_direct_doposite_form = models.FileField(upload_to='void_cheque_or_direct_doposite_forms', null=True, blank=True)
    annual_commission_statement = models.FileField(upload_to='annual_commission_statements', null=True, blank=True)
    deposit_cheque_or_receipt = models.FileField(upload_to='deposit_cheque_or_receipts', null=True, blank=True)


    def __str__(self):
        return self.username
