from django.db import models
from django.conf import settings

class CommissionAdvanceRequest(models.Model):
    ADVANCE_TYPE=[
      ('Resale Transaction','Resale Transaction'),
      ('Pre-construction','Pre-construction'),
      ('Assignment','Assignment'),
      ('Lease','Lease'),
      ('Other','Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    request_date = models.DateField(auto_now_add=True)
    advance_type = models.CharField(max_length=50,choices=ADVANCE_TYPE,default='resale')
    transaction_address = models.CharField(max_length=200)
    transaction_closing_date = models.DateField()
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_and_sale_agreement = models.FileField(upload_to='commission_advance_docs')
    waivers_of_conditions = models.FileField(upload_to='commission_advance_docs', null=True, blank=True)
    trade_record_sheet = models.FileField(upload_to='commission_advance_docs', null=True, blank=True)
    deposit_cheque_or_receipt = models.FileField(upload_to='commission_advance_docs', null=True, blank=True)
    copy_of_sold_mls_listing = models.FileField(upload_to='commission_advance_docs', null=True, blank=True)
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)