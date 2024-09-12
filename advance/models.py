from django.db import models
from django.conf import settings
from django.utils import timezone


class DocumentNote(models.Model):
  note = models.TextField()
  uploaded_at = models.DateTimeField(auto_now_add=True)
  visible_to_user = models.BooleanField(default=True)

  def __str__(self):
    return self.note
  
class Document(models.Model):
  DOCUMENT_TYPES= [
    ('Purchase and Sale Agreement','Purchase and Sale Agreement'),
    ('Waiver of Conditions','Waiver of Conditions'),
    ('Trade Record Sheet','Trade Record Sheet'),
    ('Deposit Cheque or Receipt','Deposit Cheque or Receipt'),
    ('Copy of Sold MLS Listing','Copy of Sold MLS Listing'),
    ('Other','Other')
  ]
  document = models.FileField(upload_to='commission_advance_docs')
  document_name = models.CharField(max_length=500,blank=True)
  document_type = models.CharField(max_length=50,choices=DOCUMENT_TYPES,default='resale')
  uploaded_at = models.DateTimeField(auto_now_add=True)
  notes = models.ManyToManyField(DocumentNote,blank=True)

  def __str__(self):
    return self.document


class CommissionAdvanceRequest(models.Model):
    ADVANCE_TYPE=[
      ('Resale Transaction','Resale Transaction'),
      ('Pre-construction','Pre-construction'),
      ('Assignment','Assignment'),
      ('Lease','Lease'),
      ('Other','Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('contracted', 'Contracted'),
        ('funded', 'Funded'),
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('overdue', 'Overdue'),
    ]

    FUNDING_METHOD_CHOICES = [
        ('EFT', 'Electronic Funds Transfer'),
        ('cheque', 'Cheque'),
    ]


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    request_date = models.DateField(auto_now_add=True)
    advance_type = models.CharField(max_length=50,choices=ADVANCE_TYPE,default='resale')
    transaction_address = models.CharField(max_length=200)
    transaction_closing_date = models.DateField()
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    documents = models.ManyToManyField(Document,blank=True)
    funding_method = models.CharField(max_length=10, choices=FUNDING_METHOD_CHOICES, null=True, blank=True)
    funding_date = models.DateField(null=True, blank=True)
    maturity_date = models.DateField(null=True, blank=True)
    invoice_number = models.CharField(max_length=50, null=True, blank=True)

    def days_to_maturity(self):
        if self.maturity_date:
            return (self.maturity_date - timezone.now().date()).days
        return None
    
class InvoiceItem(models.Model):
    item = models.CharField(max_length=100)
    description = models.TextField()
    qty = models.IntegerField()
    amount_per_qty = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.description

class Invoice(models.Model):
   INVOICE_STATUS = [
       ('pending', 'Pending'),
       ('paid', 'Paid'),
       ('overdue', 'Overdue'),
   ]
   advance_request = models.ForeignKey(CommissionAdvanceRequest, on_delete=models.CASCADE)
   invoice_number = models.CharField(max_length=50)
   amount = models.DecimalField(max_digits=10, decimal_places=2)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   invoice_items = models.ManyToManyField(InvoiceItem,blank=True)

   def __str__(self):
        return self.invoice_number