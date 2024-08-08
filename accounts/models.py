from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_ROLES = (
        ('Admin', 'Admin'),
        ('Broker', 'Broker'),
        ('Deal Administrator', 'Deal Administrator'),
        ('Other', 'Other'),
    )
    
    role = models.CharField(max_length=100,choices=USER_ROLES,default='Broker')
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    brokerage_name = models.CharField(max_length=100, null=True, blank=True)
    broker_of_record_name = models.CharField(max_length=100, null=True, blank=True)
    deal_administrator_name = models.CharField(max_length=100, null=True, blank=True)
    deal_administrator_email = models.EmailField(null=True, blank=True)
    driver_license = models.ImageField(upload_to='driver_licenses', null=True, blank=True)